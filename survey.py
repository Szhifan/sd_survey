import streamlit as st
import streamlit_survey as ss 
import re 
import json 
import random 
import time 
import json
import os 
random.seed(114)
# all_targets = {
#     "Migrants":{"fg_target":["illegal migrants","refugees","asylum seekers","economic migrants"],"help":None},
#     "European Union Institutions":{"tg_target":["European Parliament","European Conmission", "European Council","none"],"help":None},
#     "Migration Policies":{"fg_target":[],"help":None},
#     "Refugee Camp":["living condition","none"],
#     "Refugee Pathways":["smuglling","boat sinking","mediterranean crossing"],
#     "Asylum Procedures":["protection","compensation","refugee status","legal rights"]
# }
completion_code = "YOUR_COMPLETION_CODE"
all_targets = {
    "Turkey Agreement":{"help":"This is the agreement between Turkey and the EU signed in 2016, which states that Turkey should take measures to stop the refugees from crossing the EU-Turkey border."}, 
    "Dublin Agreement":{"help":"an EU law that determines which EU member state is responsible for processing an asylum seeker's application."}, 
    "FRONTEX":{"help":"European Border and Coast Guard Agency"},
    "FRONTEX":{"help":"European Civil Protection and Humanitarian Aid Operations"},
    "Migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants"],"help":None},
    "European Union Institutions":{"tg_targets":["none","European Parliament","European Conmission", "European Council"],"help":"Governmental Agencies at EU level, such as European Parliament, Comission and Council"},
    "refugee quotas":{"help":None},
    "refugee pathways":{"fg_targets":["none","boat sinking","mediterranean crossing","smuggling"],"help":"This includes phenomena occurring during the refugee's journey, e.g. boat sinking, smuggling, Mediterranean crossing, and so on."},
    "refugee camps":{"fg_targets":["none","living conditions"],"help":"camps to accomondate refugees"},
    "asylum procedures":{"fg_targets":["protection", "compensation", "refugee status", "legal rights", "none"],"help":"This includes legal procedures and concepts related to asylum application, e.g. protection, refugee status, legal rights, and so on"}, 

     
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
        if "valid_id" not in st.session_state:
            st.session_state["valid_id"] = False
        if "start_time" not in st.session_state:
            st.session_state["start_time"] = time.time()
        if "success" not in st.session_state:
            st.session_state["success"] = False 

    def submit_func(self):
        if st.session_state["success"]:
            st.success("submission successful!")
            dir = "anno_results/" + lang2id[self.survey_state["lang"]["value"]] + "/"
            os.makedirs(dir,exist_ok=True)
            id = self.survey_state["prolific_id"]["value"]
            path = f"id_{id}.json"
            
            self.survey.to_json(os.path.join(dir,path))
        else:
            st.error("submission failed!")
    def welcome_page(self):
    

        st.title("Multilingual Stance Detection")
        with st.container():
            st.write("Welcome to our study! You will help us annotating a SD detection dataset of tweets about the refugee crisis in the EU during 2014 and 2019.")
            id = self.survey.text_input("please enter your 24-digits prolific id and press **enter**",max_chars=24,id="prolific_id")
            if not id.isalnum() or not len(id) == 24:
            
                st.warning("invalid id")
            else: 
                st.session_state["valid_id"] = True
                st.success("id successfully submitted")
            
        with st.container():
            lang = self.survey.selectbox("please choose your language",id="lang",index=None,options=lang2id)
            if not lang: 
                st.warning("please choose a language")
        
    @staticmethod
    def reformat_ans(path:str):
        """
        reformat the survey state such that the answer for each examples is stored as: 
        {sourceID:[(target,stance)...]}
        """

    def construct_annotations(self,cur_idx):
     
        st.subheader("please determine if the following targets appear in the post, the question mark contains the definition of the target that might be helpful to you. Once you have selected a target, please determine its fine-grained target (if available) and the stance.")
        n_selected_trgt = 0 
        targets = all_targets.keys()
        # random.shuffle(list(targets))
        for t in targets:
            l_col,r_col = st.columns([2,1])
            with l_col:
                st.write(f"**{t}**")
                t_selected = self.survey.radio(t, options=["no","yes"], horizontal=True,id = f"t_{t}_{cur_idx}",help=all_targets[t]["help"])
                if t_selected == "yes":
                    n_selected_trgt += 1 
               

            with r_col:
                if t_selected == "yes":
                    s = self.survey.radio(f"stance toward _{t}_", options=["favor", "against","none"], horizontal=True,id = f"s_{t}_{cur_idx}",index=None,help="please choose none if the post doesn't express a clear stance toward the topic.")
            
                    if not s:
                        st.warning("please choose a stance")
                    else: 
         
                        st.session_state["annos_completed"][cur_idx] = True 
                        
        if not n_selected_trgt:
            st.warning("please choose at leat one target")


    def annotation_page(self,n:int):
        lang = self.survey_state["lang"]["value"]
        if lang:
            cur_idx = n - 1 
          
      
            path = f"data/{lang2id[lang]}.json"
            anno_data = get_data(path)[cur_idx]
   
            
            st.header("Please read the following tweet:")
            st.write(f"{cur_idx + 1}|{self.n_annotation}")
            with st.container(border=True):
                st.write(anno_data["fullText"])
            self.construct_annotations(cur_idx)
        else:
            st.error("please choose a language.")

    def check_success(self):
        """
        check if: 1.) the annotator entered the valid id. 2.) The annotator has completed all the examples. 3) check if they have spend enought time on the survey
        """

        success = True  
        if not st.session_state["valid_id"]:
            success = False 
            st.error("please enter a valid prolific id.")
        failed_annos = [i for i,c in enumerate(st.session_state["annos_completed"]) if not c]
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
        st.write("please ")
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
    
    sv = SDSurvey()
    sv.run_app()
    