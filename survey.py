import streamlit as st
import my_streamlit_survey as ss 
from utils import  load_anno_data,load_results,init_mongo_clinet
from interface_utils import ALL_TARGETS,TASK_DESCRIPTION,TEXT_CSS,LANG2ID
import time 
import streamlit as st
import json

class SDSurvey: 
    def __init__(self) -> None:
        new_session = self.set_qp()
        path = f"data_coder_target/{LANG2ID[self.lang]}.json"
        # translation_path = f"human_data_translated/{LANG2ID[self.lang]}.json"
  

        self.anno_data = load_anno_data(path)
        # if self.lang not in ["English","German"]:
        #     self.anno_data_translation = load_anno_data(translation_path)
        self.n_annotation = len(self.anno_data)
        self.n_pages = 1 + self.n_annotation + 1 # intro page + conclusion page + example page + annotation page 
        
        if new_session:
            user_data = load_results(self.lang,self.prolific_id,new_session)
            st.session_state["annos_completed"] = [False] * self.n_annotation
            if user_data and "completed" in user_data: #load the completion status 
                st.session_state["annos_completed"] = user_data["completed"]
            
            self.survey = ss.StreamlitSurvey("sd-survey",data=user_data) 
        self.survey = ss.StreamlitSurvey("sd-survey")
        self.pages = self.survey.pages(self.n_pages,progress_bar=True,on_submit=self.submit_func)
        self.pages.next_func = self.save_to_mongodb
        if sum(st.session_state["annos_completed"]):
            for page in range(len(st.session_state["annos_completed"])):
                if not st.session_state["annos_completed"][page]:
                    break
            self.pages.latest_page = 1 + page
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
        self.survey.data["completed"] = st.session_state["annos_completed"]
        if not client:
            st.error("connection to database failed, please try again.")
            return False
        db = client["anno-results"]
        col = db[LANG2ID[self.survey.data["LANG"]]]
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
        st.subheader("Please click :green[**introduction**] in the sidebar for more background information and domain knowledge of this task.") 
        st.subheader("Before proceeding to the annotation, it is strongly suggested that you go through the examples by clicking the sidebar :green[**examples & introdcution**] in the sidebar to the left to get yourself familiar with the interface and the expected answers. You can also refer to it when you annotate.")
        st.subheader("Your answer is automatically saved when you proceed to the next instance. You can exit the survey at anytime and resume to your lastly finished instance by clicking the :green[jump to latest] button.")
        st.subheader("Please contact us on prolific if you encounter any issues or have any questions.")

    def construct_annotations(self,cur_idx:int,example_id:str):
        """
        Display the options. 
        """
        n_selected_trgt = 0 
        targets = list(ALL_TARGETS.keys()) 
        st.session_state["annos_completed"][cur_idx] = True
        for t in targets:
            with st.container(border=True):
                l_col,r_col = st.columns([2,1])
                with l_col: 
                    fg_targets = " | ".join(ALL_TARGETS[t]["fg_targets"])
                    t_exist = self.survey.radio(f"Does target :red[{t}] exist in the post?",options=["No","Yes"],horizontal=True,id=f"e_{t}_{example_id}",help=fg_targets)
                    if t_exist == "No":
                        continue 
                    n_selected_trgt += 1
                    t_selected = self.survey.radio("Please choose a fine-grained target, choose **none** (if applicable) if only broad target exists.", options=ALL_TARGETS[t]["fg_targets"], horizontal=True,id = f"t_{t}_{example_id}",index=None)
                    
                    # if t == "migration policies" and t_selected and t_selected.startswith("p"):
                    #     t_selected = self.survey.text_input("What political entity does the post mention? (Please only answer with the entity name.)",id = f"mp_{t}_{example_id}")
                    #     if not t_selected:
                    #         st.session_state["annos_completed"][cur_idx] = False
                    #         st.warning("Please provide a political entity name and press enter.")
                    if t_selected == "none":
                         t_selected = t  
                    if not t_selected:
                        st.session_state["annos_completed"][cur_idx] = False
                        st.warning("Please choose a fine-grained target.")                  
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
        st.title(f"Annotation: {cur_idx + 1}|{self.n_annotation}")     
        
        anno_example = self.anno_data[cur_idx]
        st.header(f"id: {anno_example['resourceId']}")

        # if self.lang not in ["English","German"]:
        #     show_translation = st.checkbox("Show English Translation", value=False)
        #     if show_translation:
        #         anno_example = self.anno_data_translation[cur_idx]
        st.header("Please read the following tweet:",divider="red")
        header = st.container(border=True)
        with header:
            text = anno_example["fullText"]
            st.markdown(f"""<div class='fixed-header'>{text}""", unsafe_allow_html=True)
            st.markdown(TEXT_CSS,unsafe_allow_html=True)
        st.write(TASK_DESCRIPTION)
        self.construct_annotations(cur_idx,anno_example["resourceId"])
        self.pages.proceed_to_next = st.session_state["annos_completed"][cur_idx]
            
    def conclusion_page(self):
        st.title("Submission")
        st.write("You have successfully completed our study. Please click the submission button below to save your answers and get your **completion code**.")
        st.write("You can always go back can change your answers after submission.")
        st.header("Before submitting your annotation, we would like you answer these post-survey questions:")
        #ask the annotator how hard the task is, available options: very easy, easy, neutral, hard, very hard
        difficulty = self.survey.select_slider(label="1. How hard do you think the task is?",options=["very easy","easy","neutral","hard","very hard"],id="task_difficulty")
        # ask the annotator how much time they spent on each instance. (in minutes)
        time = self.survey.number_input("what is the total time you spent on this task? (in minutes)",min_value=0.0,key="time_spent",format="%0.1f",step=0.1)
        # more comments 
        other = self.survey.text_area("Any comments or suggestions for this task?",key="comments")
        self.survey.data["difficulty"] = difficulty
        self.survey.data["time_spent"] = time
        self.survey.data["comments"] = other
        if difficulty and time and other:
            self.pages.allow_submit = True
    def submit_func(self):
        if self.save_to_mongodb():
            st.success(f"Submission and saving successful! Please click the [completion link](https://app.prolific.com/submissions/complete?cc=CHCBTBHM) so that your work will be marked as completed. We will manually check your annotation and reward you accordingly.")  
    def run_survey(self): 
        with self.pages:
            if self.pages.current == 0:
                self.welcome_page()
                self.pages.next_button = self.pages.default_btn_next("Start!")
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