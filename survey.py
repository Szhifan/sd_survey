import streamlit as st
import my_streamlit_survey as ss 
import re 
import json  
import time 
import json
from pymongo.mongo_client import MongoClient

all_targets = {
"migration policies":{"fg_targets":["Turkey Agreement","Dublin Agreement","Refugee Quotas"],"help":"[turkey agreement](https://www.rescue.org/eu/article/what-eu-turkey-deal); [Dublin Agreement](https://en.wikipedia.org/wiki/Dublin_Regulation); refugee quotas: Ratio of refugees assigned to each EU countries during the refugee crisis."},
"migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",],"help":None},
"European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"],"help": "FRONTEX: European Border and Coast Guard Agency;ECHO:European Civil Protection and Humanitarian Aid Operations"},
"refugee pathways":{"fg_targets":["none","boat sinking","Mediterranean crossing","smuggling"],"help":"This includes phenomena occurring during the refugee's journey."},
"refugee camps":{"fg_targets":["none","living conditions"],"help":"camps to accommodate refugees"},
"asylum procedures":{"fg_targets":["none","protection", "compensation", "refugee status", "legal rights"],"help":"This includes legal procedures and concepts related to asylum application."},
} 
lang2id = {"English":"en","German":"de","Greek":"el","Spanish":"es","French":"fr","Hungarian":"hu","Italian":"it","Dutch":"nl","Polish":"pl","Slovak":"sk","Swedish":"sv"}
stance_options = ["favor","against","none"]
ttl = 1200
@st.cache_data(ttl=ttl)
def get_data(path:str):
    with open(path,"r") as f:
        return json.load(f)

@st.cache_resource(ttl=ttl)
def init_mongo_clinet() -> MongoClient:
    
    # Create a new client and connect to the server
    client = MongoClient(st.secrets["uri"])
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return client 
    except Exception:
        return None 
    

def load_results_no_cache(lang,id):

    client = init_mongo_clinet()
    if not client:
        st.warning("connection to database failed, please try again.")
        return None 
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    user_data = col.find_one(query)
    return user_data 
@st.cache_data(ttl=ttl,show_spinner="loading your previously stored results")
def load_results_cache(lang,id):
 
    client = init_mongo_clinet()
    if not client:
        st.warning("connection to database failed, please try again.")
        return None 
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    user_data = col.find_one(query)
    return user_data 

def load_results(lang,id,use_cache=False):
   
    return load_results_no_cache(lang,id) if use_cache else load_results_cache(lang,id)
    


class SDSurvey: 
    def __init__(self) -> None:
        new_session = self.set_qp()
        path = f"data/{lang2id[self.lang]}.json"
        self.anno_data = get_data(path)
        self.n_annotation = len(self.anno_data)
        self.n_pages =1 + self.n_annotation + 1 # intro page + conclusion page + example page + annotation page 
        user_data = load_results(self.lang,self.prolific_id,use_cache=new_session)
        if "annos_completed" not in st.session_state:  # check if an annotation is successfull completed. Criterion: for each example, at least one target must be choosen. For each choosen target, a stance must be choosen. 
            st.session_state["annos_completed"] = [False] * self.n_annotation
            if user_data and "completed" in user_data: #load the completion status 
                st.session_state["annos_completed"] = [i < user_data["completed"] for i in range(self.n_annotation)]
        self.survey = ss.StreamlitSurvey("sd-survey",data=user_data)
        self.pages = self.survey.pages(self.n_pages,progress_bar=True,on_submit=self.submit_func)
        if sum(st.session_state["annos_completed"]):
            self.pages.latest_page = 1 + sum(st.session_state["annos_completed"])
           
    def set_qp(self):
        """
        save the query parameters to session state for reuse.
        return :new_session. If it is a new session or not  
        """
        new_session = False 
        if "qp" not in st.session_state:
            new_session = True 
            st.session_state["qp"] = st.query_params.to_dict()  
            
        if len(st.session_state["qp"]): 
            self.lang = st.session_state["qp"]["LANG"]   
            self.prolific_id = st.session_state["qp"]["PROLIFIC_PID"]
            self.study_id = st.session_state["qp"]["STUDY_ID"]  
        else:
            self.lang = st.session_state["qp"]["LANG"] = "English"
            self.prolific_id = st.session_state["qp"]["PROLIFIC_PID"] = "default_prolific_id"
            self.study_id = st.session_state["qp"]["STUDY_ID"]  = "default_study_id"
        st.query_params.from_dict(st.session_state["qp"])     
        return new_session 

    def save_to_mongodb(self):
        """
        save or update the annotation results based on prolific_id 
        """
        client = init_mongo_clinet()
        self.survey.data["LANG"] = self.lang
        self.survey.data["PROLIFIC_PID"] = self.prolific_id
        self.survey.data["completed"] = sum(st.session_state["annos_completed"])
        if not client:
            st.error("connection to database failed, please try again.")
            return 
        db = client["anno-results"]
        col = db[lang2id[self.survey.data["LANG"]]]
        query = {"PROLIFIC_PID":self.survey.data["PROLIFIC_PID"]}
        update = {"$set":self.survey.data}

        if not col.find_one(query):
            col.insert_one(self.survey.data)
        else:
            col.update_one(query,update)
        st.success("results saved")

  
    @staticmethod
    def reformat_ans(data):
        """
        reformat the survey state such that the answer for each examples is stored as: 
        {sourceID:[(target,stance)...]}
        """

    def set_state(self,cur_idx:int,choise="No selection"):
        """
        check if a valid answer is selected
        """
        if "annos_completed" in st.session_state:
            st.session_state["annos_completed"][cur_idx] = (choise!="No selection")
        
  

    def welcome_page(self):
        """draw the first welcome page"""
        
        st.sidebar.success("have a look at the examples and instructions!")
        st.title("Stance Detection: Refugee Crisis")
    
        st.header("Welcome to our study!")
        st.write("Before proceeding to the annotation, it is strongly suggested that you go through the examples by clicking the sidebar **examples&instruction** to the left to get yourself familiar with the interface and the expected answers. You can also refer to it when you annotate.")
        st.write("If you wish to take a rest, you can push the **save** button to the top-left corner of the annotation page.")
        
        
     
    def construct_annotations(self,cur_idx,example_id):
        """
        Display the options
        """
     
        st.write("Please determine if the following targets appear in the post, the question mark contains the definition of the target that might be helpful to you. Once you have selected a target, please determine its fine-grained target (if available) and the stance. You can choose up to **three** targets.")
        n_selected_trgt = 0 
        targets = all_targets.keys()
        # random.shuffle(list(targets))
        for t in targets:
            with st.container(border=True):
                l_col,r_col = st.columns([2,1])
                with l_col: 
                    st.subheader(f"{t}",help=all_targets[t]["help"])
                    t_selected = self.survey.radio("Please choose a fine-grained target, choose 'none' (if applicable) if only broad target exists.", options=["No selection"] + all_targets[t]["fg_targets"], horizontal=True,id = f"t_{t}_{cur_idx}")
                    if t_selected != "No selection":
                        n_selected_trgt += 1 
                

                with r_col:
                    if t_selected != "No selection":
                        s_selected = self.survey.radio(f"stance toward _{t_selected}_", options=["No selection"] + ["favor", "against","none"], horizontal=True,id = f"s_{t}_{cur_idx}",help="please choose none if the post doesn't express a clear stance toward the topic.")
                
                        if s_selected == "No selection":
                            st.warning("Please choose a stance.")
                        self.set_state(cur_idx,s_selected)            
        if not n_selected_trgt:
            st.session_state["annos_completed"][cur_idx] = False
            st.warning("Please choose at least one target.")
        if n_selected_trgt > 3:
            st.session_state["annos_completed"][cur_idx] = False
            st.warning("You can only choose up to three targets.")
    def annotation_page(self,n:int):
        '''
        Display the annotation page. 
        '''

        st.title("Annotation")
        cur_idx = n - 1 
        btn = st.button("save results",key="save_btn_" + str(cur_idx),help="please click to save the results.")
        if btn:
            self.save_to_mongodb()
        
        anno_example = self.anno_data[cur_idx]
       
        st.header("Please read the following tweet:",divider="red")
        st.write(f"{cur_idx + 1}|{self.n_annotation}")
        with st.container(border=True):
            st.subheader(anno_example["fullText"])
        
        self.construct_annotations(cur_idx,anno_example["resourceId"])
        
        self.pages.proceed_to_next =  st.session_state["annos_completed"][cur_idx]

    def last_page(self):
        st.title("Submission")
        st.write("You have successfully completed our study. Please click the submission button below to save your answers get your **completion code**.")
        st.write("If you have any suggestions for our survey. Please feel free to reach out to us in Prolific, we would appreciate your feedback!")
    def submit_func(self):
        
        if self.save_to_mongodb(self.survey.data):
            st.success("Submission and saving successful! Please click the [completion link](https://app.prolific.com/submissions/complete?cc=CHCBTBHM) to mark your completion.")
     
    def run_app(self):
        with self.pages:
            if self.pages.current == 0:
                self.welcome_page()
            elif self.pages.current ==self.n_pages-1:
                self.last_page()
            else:
                self.annotation_page(self.pages.current)
if __name__ == "__main__":
    
    st.set_page_config("Stance Detection Annotation",layout="wide")
    sv = SDSurvey()
    sv.run_app()
    