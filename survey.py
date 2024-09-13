import streamlit as st
import my_streamlit_survey as ss 
from utils import  *
import random 
import time 
class SDSurvey: 
    def __init__(self) -> None:
        new_session = self.set_qp()
        path = f"data/{lang2id[self.lang]}.json"
        self.anno_data = get_anno_data(path)
        self.n_annotation = len(self.anno_data)
        self.n_pages =1 + self.n_annotation + 1 # intro page + conclusion page + example page + annotation page 
        user_data = load_results(self.lang,self.prolific_id,use_cache=new_session)
        if "time_start" not in user_data:
            user_data["time_start"] = time.time()
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
        save or update the annotation results based on prolific_id  and language 
        """
        client = init_mongo_clinet()
        self.survey.data["LANG"] = self.lang
        self.survey.data["PROLIFIC_PID"] = self.prolific_id
        self.survey.data["completed"] = sum(st.session_state["annos_completed"])
        if not client:
            st.error("connection to database failed, please try again.")
            return False
        db = client["anno-results"]
        col = db[lang2id[self.survey.data["LANG"]]]
        query = {"PROLIFIC_PID":self.survey.data["PROLIFIC_PID"]}
        update = {"$set":self.survey.data}
        if not col.find_one(query):
            col.insert_one(self.survey.data)
        else:
            col.update_one(query,update)
        st.success("results saved")
        return True
    def welcome_page(self):
        """draw the first welcome page"""

        st.title("Stance Detection: Refugee Crisis")
    
        st.header("Welcome to our study!")
        st.subheader("Please click :green[**introduction**] for more background information and domain knowledge of this task.") 
        st.subheader("Before proceeding to the annotation, it is strongly suggested that you go through the examples by clicking the sidebar :green[**examples & dinstruction**] to the left to get yourself familiar with the interface and the expected answers. You can also refer to it when you annotate.")
        st.subheader("Your answer is automatically saved when you proceed to the next instance. You can exit the survey at anytime and resume to your lastly finished instance by clicking the :green[jump to latest] button")
    def construct_annotations(self,cur_idx:int,example_id:str,anno_example:str):
        """
        Display the options
        """
        n_selected_trgt = 0 
        targets = list(all_targets.keys()) 
        st.session_state["annos_completed"][cur_idx] = True
    
        for t in targets:
            with st.container(border=True):
                with st.container():
                    st.subheader(anno_example,divider="orange") 
                l_col,r_col = st.columns([2,1])
                with l_col: 
            
                    t_exist = self.survey.radio(f"Does target :red[{t}] exist in the post?",options=["No","Yes"],horizontal=True,id=f"e_{t}_{example_id}")
                    if t_exist == "No":
                        continue 
                    n_selected_trgt += 1
                    t_selected = self.survey.radio("Please choose a fine-grained target, choose **none** (if applicable) if only broad target exists.", options=all_targets[t]["fg_targets"], horizontal=True,id = f"t_{t}_{example_id}",index=None)

                    if t == "migration policies" and t_selected and t_selected.startswith("p"):
                        t_selected = self.survey.text_input("What political entity does the post mention? (Please only answer with the entity name.)",id = f"mp_{t}_{example_id}")
                        if not t_selected:
                            st.session_state["annos_completed"][cur_idx] = False
                            st.warning("Please provide a political entity name and press enter.")
                    if t_selected == "none":
                         t_selected = t                    
                with r_col:
                    if t_selected:
                        s_selected = self.survey.radio(f"stance toward _:red[{t_selected}]_", options=["favor", "against","none"], horizontal=True,id = f"s_{t}_{example_id}",index=None)
                
                        if not s_selected:
                            st.session_state["annos_completed"][cur_idx] = False
                            st.warning("Please choose a stance.")                          
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

        cur_idx = n - 1 
        if cur_idx and st.session_state["annos_completed"][cur_idx -1]:
            self.save_to_mongodb()
        st.title(f"Annotation: {cur_idx + 1}|{self.n_annotation}")     
        anno_example = self.anno_data[cur_idx]
       
        st.header("Please read the following tweet:",divider="red")
        st.write(task_description)
        self.construct_annotations(cur_idx,anno_example["resourceId"],anno_example["fullText"])
        self.pages.proceed_to_next =  st.session_state["annos_completed"][cur_idx]
    def conclusion_page(self):
        st.title("Submission")
        st.write("You have successfully completed our study. Please click the submission button below to save your answers and get your **completion code**.")
        st.write("You can always go back can change your answers after submission.")
        st.write("If you have any have suggestions for our survey. Please feel free to reach out to us on Prolific, your feedback is valuable for us!")
    def submit_func(self):
        try:
            self.survey.data["time_spent"] = (time.time() - self.survey.data["time_start"]) / 60
            
        except KeyError:
            pass 
        if self.save_to_mongodb():
            st.success(f"Submission and saving successful! Please click the [completion link](https://app.prolific.com/submissions/complete?cc=CHCBTBHM) so that your work will be marked as completed. We will manually check your annotation and reward you accordingly.")  
    def run_survey(self):
        with self.pages:
            if self.pages.current == 0:
                self.welcome_page()
            elif self.pages.current ==self.n_pages-1:
                self.conclusion_page()
            else:
                self.annotation_page(self.pages.current)
    
def main():
    st.set_page_config(layout="wide")
    sv = SDSurvey()
    sv.run_survey()
if __name__ == "__main__":

    main_page = st.Page(page=main,title="Stance detection annotation",icon="✒️")
    instructions = st.Page(page="stranicy/introduction.py",title="introduction",icon="💡")
    examples = st.Page(page="stranicy/examples.py",title="examples & instructions",icon="📖")
    pg = st.navigation([main_page,instructions,examples])
    pg.run()