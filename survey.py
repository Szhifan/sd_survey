import streamlit as st
import streamlit_survey as ss 
import re 
import json 
import random 
import time 
import json
from pymongo.mongo_client import MongoClient
import os 
random.seed(114)
completion_link = "https://app.prolific.com/submissions/complete?cc=CHCBTBHM"

all_targets = {
"migration policies":{"fg_targets":["Turkey Agreement","Dublin Agreement","Refugee Quotas"],"help":"[turkey agreement](https://www.rescue.org/eu/article/what-eu-turkey-deal); [Dublin Agreement](https://en.wikipedia.org/wiki/Dublin_Regulation); refugee quotas: Ratio of refugees assigned to each EU countries during the refugee crisis."},
"migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",],"help":None},
"European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"],"help": "FRONTEX: European Border and Coast Guard Agency;ECHO:European Civil Protection and Humanitarian Aid Operations"},
"refugee pathways":{"fg_targets":["none","boat sinking","Mediterranean crossing","smuggling"],"help":"This includes phenomena occurring during the refugee's journey."},
"refugee camps":{"fg_targets":["none","living conditions"],"help":"camps to accommodate refugees"},
"asylum procedures":{"fg_targets":["none","protection", "compensation", "refugee status", "legal rights"],"help":"This includes legal procedures and concepts related to asylum application."},
} 
stance_options = ["favor","against","none"]
@st.cache_data()
def get_data(path:str):
    with open(path,"r") as f:
        return json.load(f)
lang2id = {"English":"en","German":"de","Greek":"el","Spanish":"es","French":"fr","Hungarian":"hu","Italian":"it","Dutch":"nl","Polish":"pl","Slovak":"sk","Swedish":"sv"}
@st.cache_resource
def init_mongo_clinet() -> MongoClient:
    
    # Create a new client and connect to the server
    client = MongoClient(st.secrets["uri"])
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return client 
    except Exception as e:
        return None 
    

def load_user_data(lang,id):
    client = init_mongo_clinet()
    if not client:
        st.warning("connection to database failed, please try again.")
        return None 
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    user_data = col.find_one(query)
    
    return user_data 


class SDSurvey: 
    def __init__(self,name="sd-survey") -> None:
       
        self.set_qp()
        self.success = False 
   
        self.n_annotation = 4

        
        self.n_pages =1 + self.n_annotation + 1 # intro page + conclusion page + example page + annotation page 
        
        # self.estimated_completion_time = 20 # the estimated completion time (in second) if the annotator spends less than this, he or she will not be marked as completed 
       
        if "annos_completed" not in st.session_state:  # check if an annotation is successfull completed. Criterion: for each example, at least one target must be choosen. For each choosen target, a stance must be choosen. 
            st.session_state["annos_completed"] = [False] * self.n_annotation
        if "start_time" not in st.session_state:
            st.session_state["start_time"] = time.time()
        if "success" not in st.session_state:
            st.session_state["success"] = False 


    
            
        user_data = load_user_data(self.lang,self.prolific_id)
       
        if user_data and "__streamlit-survey-data" + "_" + name not in st.session_state:
            st.session_state["__streamlit-survey-data" + "_" + name] = user_data
        
        self.survey = ss.StreamlitSurvey(name)
        self.survey_state = self.survey.data
        self.pages = self.survey.pages(self.n_pages,progress_bar=True,on_submit=self.submit_func)
    
        
        
    def set_qp(self):
        
        if "qp" not in st.session_state:
            st.session_state["qp"] = st.query_params.to_dict()  
        if len(st.session_state["qp"]): 
            self.lang = st.session_state["qp"]["LANG"]   
            self.prolific_id = st.session_state["qp"]["PROLIFIC_PID"]
            self.study_id = st.session_state["qp"]["STUDY_ID"]  
  
        else: #if there is no qp 
            self.lang = "English"
            self.prolific_id = "default_prolific_id"  
            self.study_id = "default_study_id"
        st.query_params.from_dict(st.session_state["qp"])     

    def save_to_mongodb(self):
        """
        save or update the annotation results based on prolific_id 
        """
        client = init_mongo_clinet()
        self.survey_state["LANG"] = self.lang
        self.survey_state["PROLIFIC_PID"] = self.prolific_id
        if not client:
            st.warning("connection to database failed, please try again.")
            return 
        db = client["anno-results"]
        col = db[lang2id[self.survey_state["LANG"]]]
        query = {"PROLIFIC_PID":self.survey_state["PROLIFIC_PID"]}
        update = {"$set":self.survey_state}

        if not col.find_one(query):
            col.insert_one(self.survey_state)
        else:
            col.update_one(query,update)
        st.success("results saved")
    def submit_func(self):
        if st.session_state["success"]:
            


            self.save_to_mongodb(self.survey_state)
            st.success("submission and saving successful! Please click the [completion link](https://app.prolific.com/submissions/complete?cc=CHCBTBHM) to mark your completion.")

            
        else:
            st.error("submission failed!")
  
    @staticmethod
    def reformat_ans(path:str):
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
        """draw the first welcom page"""
        st.sidebar.success("have a look at the examples and instructions!")
        self.pages.n_page_completed[0] = True

  

        st.title("Stance Detection: Refugee Crisis 2015")
    
        st.header("Welcome to our study!")
        
        st.write("Before proceeding to the annotation, it is strongly suggested that you go through the examples by clicking the sidebar **examples&instruction** to the left to get yourself familiar with the interface and the expected answers. You can also refer to it when you annotate.")
        st.write("please note that once you start the annotation you cannot close the browser window as the results will lose.")
   
        
     
    def construct_annotations(self,cur_idx):
     
        st.write("please determine if the following targets appear in the post, the question mark contains the definition of the target that might be helpful to you. Once you have selected a target, please determine its fine-grained target (if available) and the stance. You can choose up to **three** targets")
        n_selected_trgt = 0 
        targets = all_targets.keys()
        # random.shuffle(list(targets))
        for t in targets:
            with st.container(border=True):
                l_col,r_col = st.columns([2,1])
                with l_col: 
                    st.subheader(f"{t}",help=all_targets[t]["help"])
                    t_selected = self.survey.radio("please choose a fine-grained target, choose 'none' (if applicable) if only broad target exists.", options=["No selection"] + all_targets[t]["fg_targets"], horizontal=True,id = f"t_{t}_{cur_idx}")
                    if t_selected != "No selection":
                        n_selected_trgt += 1 
                

                with r_col:
                    if t_selected != "No selection":
                        s_selected = self.survey.radio(f"stance toward _{t_selected}_", options=["No selection"] + ["favor", "against","none"], horizontal=True,id = f"s_{t}_{cur_idx}",help="please choose none if the post doesn't express a clear stance toward the topic.")
                
                        if s_selected == "No selection":
                            st.warning("please choose a stance.")
                        self.set_state(cur_idx,s_selected)            
        if not n_selected_trgt:
            self.set_state(cur_idx)
            st.warning("please choose at least one target.")
        if n_selected_trgt > 3:
            self.set_state(cur_idx)
            st.warning("you can only choose up to three targets")
        


    def annotation_page(self,n:int):

        st.title("Annotation")
        cur_idx = n - 1 
        btn = st.button("save results",key="save_btn_" + str(cur_idx))
        if btn:
            self.save_to_mongodb()
        path = f"data/{lang2id[self.lang]}.json"
        anno_data = get_data(path)[cur_idx]
        if cur_idx and not st.session_state["annos_completed"][cur_idx-1]:
            st.error("You haven't completed the last annotation, please go back.")
        else:
            st.header("Please read the following tweet:",divider="red")
            st.write(f"{cur_idx + 1}|{self.n_annotation}")
            with st.container(border=True):
                st.subheader(anno_data["fullText"])
            self.construct_annotations(cur_idx)
        
        self.pages.n_page_completed[n] =  st.session_state["annos_completed"][cur_idx]

    def check_success(self):
        """
        check if: 1.) the annotator entered the valid id. 2.) The annotator has completed all the examples. 3) check if they have spend enought time on the survey
        """

        success = True  
     
        failed_annos = [i + 1 for i,c in enumerate(st.session_state["annos_completed"]) if not c]
        if len(failed_annos):
            success = False 
            st.error(f"you have not completed example(s): {failed_annos}")
        # time_spent = time.time() - st.session_state["start_time"]
        # if "time_spent" not in self.survey_state:
        #     self.survey_state["time_spent"] = time_spent 

        # if  time_spent <= self.estimated_completion_time:
        #     success = False 
        #     st.error(f"you should spend at least {round(self.estimated_completion_time / 60,2)} minutes on the task. There are still {round((self.estimated_completion_time - time_spent) / 60,2)} minutes left.")
        if success: 
            st.success(f"Congradualations, you have successfully completed the survey, please click the submit button.")
        return success 


    def last_page(self):
        st.title("Submission")
        st.write("we are checking your response. Upon successful completion, you will receive a **completion link**, please click the link to mark your completion.")
        st.write("If you have any suggestions for our survey. Please feel free to reach out to us in Prolific, we would appreciate your feedback!")
        st.session_state["success"] = self.check_success()
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
    