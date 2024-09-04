import streamlit as st
import streamlit_survey as ss 
import re 
import json 
import random 
import time 
import json
import os 
random.seed(114)

completion_code = "YOUR_COMPLETION_CODE"
all_targets = {
    "Turkey Agreement":{"fg_targets":["Turkey Agreement"],"help":"[Click the link for more information:](https://www.rescue.org/eu/article/what-eu-turkey-deal)"}, 
    "Dublin Agreement":{"fg_targets":["Dublin Agreement"],"help":"[Click the link for more information:](https://en.wikipedia.org/wiki/Dublin_Regulation)"}, 
    "Migrants":{"fg_targets":["migrants","illegal migrants","refugees","asylum seekers","economic migrants",],"help":None},
    "European Union Institutions":{"fg_targets":["European Union Institutions","European Parliament","European Conmission", "European Council","FRONTEX","ECHO"],"help":"FRONTEX:European Border and Coast Guard Agency;ECHO:European Civil Protection and Humanitarian Aid Operations"},
    "refugee quotas":{"fg_targets":["refugee quotas"],"help":"Ratio of refugees assigned to each EU countries during the refugee crisis."},
    "refugee pathways":{"fg_targets":["refugee pathways","boat sinking","mediterranean crossing","smuggling"],"help":"This includes phenomena occurring during the refugee's journey."},
    "refugee camps":{"fg_targets":["refugee camps","living conditions"],"help":"camps to accomondate refugees"},
    "asylum procedures":{"fg_targets":["asylum procedures","protection", "compensation", "refugee status", "legal rights"],"help":"This includes legal procedures and concepts related to asylum application."}, 

     
}
stance_options = ["favor","against","none"]
@st.cache_data()
def get_data(path:str):
    with open(path,"r") as f:
        return json.load(f)
lang2id = {"English":"en","German":"de","Greek":"el","Spanish":"es","French":"fr","Hungarian":"hu","Italian":"it","Dutch":"nl","Polish":"pl","Slovak":"sk","Swedish":"sv"}
class SDSurvey: 
    def __init__(self) -> None:
        self.success = False 
        self.survey = ss.StreamlitSurvey("sd annotation survey")
        self.survey_state = self.survey.data 
        self.n_annotation = 4

        self.n_pages = self.n_annotation + 2 # intro page + conclusion page + example page + annotation page 
        self.pages = self.survey.pages(self.n_pages,progress_bar=True,on_submit=self.submit_func)
        self.estimated_completion_time = 20 # the estimated completion time (in second) if the annotator spends less than this, he or she will not be marked as completed 
       
        if "annos_completed" not in st.session_state:  # check if an annotation is successfull completed. Criterion: for each example, at least one target must be choosen. For each choosen target, a stance must be choosen. 
            st.session_state["annos_completed"] = [False] * self.n_annotation
        if "start_time" not in st.session_state:
            st.session_state["start_time"] = time.time()
        if "success" not in st.session_state:
            st.session_state["success"] = False 
        self.set_qp()

        
    def set_qp(self):
        
        if "qp" not in st.session_state:
            st.session_state["qp"] = st.query_params.to_dict()  
        if len(st.session_state["qp"]): 
            self.lang = st.session_state["qp"]["LANG"]   
            self.prolific_id = st.session_state["qp"]["PROLIFIC_PID"]  
  
        else: #if there is no qp 
            self.lang = "English"
            self.prolific_id = "prolific_id"  
        st.query_params.from_dict(st.session_state["qp"])     
    

    def submit_func(self):
        if st.session_state["success"]:
            st.success("submission successful!")
            dir = "anno_results/" + lang2id[self.survey_state["LANG"]["value"]] + "/"
            os.makedirs(dir,exist_ok=True)
            path = f"id_{id}.json"
            
            self.survey.to_json(os.path.join(dir,path))
        else:
            st.error("submission failed!")
          
    @staticmethod
    def reformat_ans(path:str):
        """
        reformat the survey state such that the answer for each examples is stored as: 
        {sourceID:[(target,stance)...]}
        """
    def set_state(self,cur_idx:int,choise="NA"):
        """
        check if a valid answer is selected
        """
        if "annos_completed" in st.session_state:
            st.session_state["annos_completed"][cur_idx] = (choise!="NA")
  

    def welcome_page(self):
        """draw the first welcom page"""
        st.sidebar.success("have a look at the examples and instructions!")

        example = {"text":["Blessed are the peacemakers, for they shall be called children of God. Matthew 5:9 #scripture #peace #SemST"],"target":["Atheism"],"stance":["against"]}

        st.title("Stance Detection: Refugee Crisis 2015")
    
        st.header("Welcome to our study!")
        st.write("You are tasked with annotating a stance detection dataset about the refugee crisis in the EU during 2014 and 2019. A stance detection dataset typically includes target and stance. A target is the topic in a piece of text while a stance is associated with the target. Here is an example from [semeval-2016](https://www.saifmohammad.com/WebPages/StanceDataset.htm)")
        with st.container(border=True):
            st.table(example)
        st.write("You are tasked with annotating a stance detection dataset about the refugee crisis in the EU during 2014 and 2019. A stance detection dataset typically includes target(s) and stance, where the target is the topic of the text and the stance is the position of the author of the text toward the target. In our dataset, we introduce the distinction between target and fine-grained target. A fine-grained target is usually the hyponym of its corresponding target. For instance, “refugee” is the fine-grained target of “migrants”. Before proceeding to the annotation, it is strongly suggested that you go through the examples by clicking the sidebar **examples&instruction** to the left to get yourself familiar with the interface and the expected answers. You can also refer to it when you annotate.")
    
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
                    t_selected = self.survey.radio("please choose a fine-grained target (if applicable)", options=["NA"] + all_targets[t]["fg_targets"], horizontal=True,id = f"t_{t}_{cur_idx}")
                    if t_selected != "NA":
                        n_selected_trgt += 1 
                

                with r_col:
                    if t_selected != "NA":
                        s_selected = self.survey.radio(f"stance toward _{t_selected}_", options=["NA"] + ["favor", "against","none"], horizontal=True,id = f"s_{t}_{cur_idx}",help="please choose none if the post doesn't express a clear stance toward the topic.")
                
                        if s_selected == "NA":
                            st.warning("please choose a stance")
                        self.set_state(cur_idx,s_selected)
        
           
 
                        
        if not n_selected_trgt:
            self.set_state(cur_idx)
            st.warning("please choose at leat one target")
        if n_selected_trgt > 3:
            self.set_state(cur_idx)
            st.warning("you can only choose up to three targets")
            


    def annotation_page(self,n:int):
        st.title("Annotation")
        cur_idx = n - 1 
        path = f"data/{lang2id[self.lang]}.json"
        anno_data = get_data(path)[cur_idx]

        
        st.header("Please read the following tweet:",divider="red")
        st.write(f"{cur_idx + 1}|{self.n_annotation}")
        with st.container(border=True):
            st.subheader(anno_data["fullText"])
        self.construct_annotations(cur_idx)


    def check_success(self):
        """
        check if: 1.) the annotator entered the valid id. 2.) The annotator has completed all the examples. 3) check if they have spend enought time on the survey
        """

        success = True  
     
        failed_annos = [i + 1 for i,c in enumerate(st.session_state["annos_completed"]) if not c]
        if len(failed_annos):
            success = False 
            st.error(f"you have not completed example(s): {failed_annos}")
        time_spent = time.time() - st.session_state["start_time"]
        if "time_spent" not in self.survey_state:
            self.survey_state["time_spent"] = time_spent 

        if  time_spent <= self.estimated_completion_time:
            success = False 
            st.error(f"you should spend at least {round(self.estimated_completion_time / 60,2)} minutes on the task. There are still {round((self.estimated_completion_time - time_spent) / 60,2)} minutes left.")
        if success: 
            st.success(f"Congradualations, you have successfully completed the survey, here is your completion code: **{completion_code}**")
        return success 


    def last_page(self):
        st.title("Submission")
        st.write("we are checking your response. Upon successful completion, you will receive a completion code, which marks your completion and you will be rewarded accordingly.")
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
    