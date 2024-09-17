import streamlit as st 
import my_streamlit_survey as ss
from utils import *



class EvalSurvey():
    def __init__(self,id,lang) -> None:
        self.id = id 
        self.lang = lang
        
        if "new_session" not in st.session_state:
            st.session_state["new_session"] = True
        else:
            st.session_state["new_session"] = False
        self.data = load_anno_result(id,lang,st.session_state["new_session"])
        if not self.data:
            st.error("No data found for this language and id")
        # load completed evaluation example and score. If it is not present, create it.
        if "completed" not in self.data:    
            self.data["completed"] = [False] * len(self.data["results"])
            self.data["score"] = [0] * len(self.data["results"])
        # put completion and score status to session state if it is not present.
        if "completed" not in st.session_state:
            st.session_state["completed"] = self.data["completed"]
        if "score" not in st.session_state:
            st.session_state["score"] = self.data["score"]
        # create a survey object for evaluation.
        self.survey = ss.StreamlitSurvey("evaluation",data=self.data["survey_state"] if "survey_state" in self.data else None)
        self.pages = self.survey.pages(len(self.data["results"]) + 1,progress_bar=True,on_submit=self.save)
   
        if sum(self.data["completed"]):
            self.pages.latest_page = sum(self.data["completed"])
        self.total_score = len(self.data["results"]) * 4
    def save(self):

        path = f"anno_results/{lang2id[self.lang]}/{self.id}.json"
        self.data["completed"] = st.session_state["completed"]
        self.data["score"] = st.session_state["score"]
        self.data["survey_state"] =  self.survey.data 

        with open(path,"w") as f:
            json.dump(self.data,f)
        st.success("Data saved successfully")
    def eval_page(self,page_idx):
        """
        Display the evaluation page for the given page index. 
        set the passed status for the given page index to true if the user has passed the evaluation.  
        """
        results = self.data["results"]
        cur_example_id = list(results.keys())[page_idx]
        text = get_text_by_id(cur_example_id,self.lang)
        annos = self.data["results"][cur_example_id]
        eval_res = ["crap","bad","ok","good","excellent"]
        

        col_l,col_r = st.columns(2)
        with col_l:
            st.header(f"Example {page_idx+1}/{len(results)}")
        with col_r:
            st.header(f"prolific_id: {self.id}")
        with st.container(border=True):
            st.header(text)
        for anno in annos:
            target = anno[0]
            stace = anno[1]
            with st.container(border=True):
                st.write(f"target: {target}")
                st.write(f"stace: {stace}") 
        pass_btn = self.survey.radio(label="how do you like it?",options=eval_res,id=cur_example_id,horizontal=True)
        score = eval_res.index(pass_btn) 
        st.session_state["score"][page_idx] = score
        st.session_state["completed"][page_idx] = True
      
        self.save()
        # display score 
        st.subheader(f"curent score: {sum(st.session_state['score'])}/{self.total_score}")
    def conclusion_page(self):
        """
        Display the total score and decide if the answer should be accepted or not. 
        """
        total_score = sum(st.session_state["score"])
        st.header("Evaluation completed")
        st.subheader(f"Total score: {total_score}/{self.total_score}")
        pss = self.survey.radio("Accept the evaluation",options=["Yes","No"],id="accept",index=None) 
        
    def run(self):
        """
        Main function to launch the evaluation interface 
        """

        with self.pages:
            if self.pages.current < len(self.data["results"]):
                self.eval_page(self.pages.current)
            else:
                self.conclusion_page()
            



    

if __name__ == "__main__":
    eval = EvalSurvey("default_prolific_id","English") 
    eval.run()