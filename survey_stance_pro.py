import streamlit as st
import my_streamlit_survey as ss 
from utils import  load_anno_data,load_results,init_mongo_clinet,load_anno_data_partition
from interface_utils import LANG2ID,TEXT_CSS,TASK_DESCRIPTION_STANCE,TARGETS_MAP,RELEVANT_CHOICES,STANCE_OPTIONS,ATTENTION_TESTS
import streamlit as st
from introduction_stance import display
# version two partition the data into two parts.
class SDSurvey: 
    def __init__(self) -> None:
        new_session = self.set_qp()
        path = f"data_coder_stance/{LANG2ID[self.lang]}.json"  
        path_translated = "data_coder_stance/translated.json"
        
        self.data_translated = load_anno_data(path_translated)
        self.attention_test = ATTENTION_TESTS[LANG2ID[self.lang]]
        self.n_attention_test = len(self.attention_test)
        self.anno_data = load_anno_data_partition(path,n=400,partition=self.partition)

        self.n_annotation = len(self.anno_data)
        self.n_pages = 1 + self.n_annotation + 1 # intro page + conclusion page + annotation page 
        if new_session:
            user_data = load_results(self.lang,self.prolific_id,new_session,db_name="anno-stance",study_id=self.study_id)
            st.session_state["annos_completed"] = [False] * self.n_annotation
            st.session_state["test_passed"] = [False] * self.n_attention_test
            if user_data and "completed" in user_data: #load the completion status 
                st.session_state["annos_completed"] = user_data["completed"]
            if user_data and "test_passed" in user_data:
                st.session_state["test_passed"] = user_data["test_passed"]
            self.survey = ss.StreamlitSurvey("sd-survey",data=user_data) 
        self.survey = ss.StreamlitSurvey("sd-survey")
        self.pages = self.survey.pages(self.n_pages,progress_bar=True,on_submit=self.submit_func)
        self.pages.next_func = self.save_to_mongodb
        if sum(st.session_state["annos_completed"]):
            for page in range(len(st.session_state["annos_completed"])-1):
                if not st.session_state["annos_completed"][page]:
                    break
            self.pages.latest_page = 190
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
            self.partition = st.session_state["qp"]["PARTITION"]
        else:
            self.lang = st.session_state["qp"]["LANG"] = "English"
            self.prolific_id = st.session_state["qp"]["PROLIFIC_PID"] = "default_prolific_id"
            self.study_id = st.session_state["qp"]["STUDY_ID"]  = "default_study_id"
            self.partition = st.session_state["qp"]["PARTITION"] = 0
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
        self.survey.data["test_passed"] = st.session_state["test_passed"]
        self.survey.data["study_id"] = self.study_id
        self.survey.data["partition"] = self.partition
        if not client:
            st.error("connection to database failed, please try again.")
            return False
        db = client["anno-stance"]
        col = db[LANG2ID[self.survey.data["LANG"]]]
        query = {
                "PROLIFIC_PID":self.survey.data["PROLIFIC_PID"],
                "study_id":self.survey.data["study_id"]
                }
        update = {"$set":self.survey.data}
        querried = col.find_one(query)
        try:
            if not querried:
                col.insert_one(self.survey.data)
            else:
                col.update_one(query,update)
        except Exception as e:
            st.error(f"Error saving results: {e}")
            return False
        st.success("results saved")
        return True
    def welcome_page(self):
        """draw the first welcome page"""

        st.title("Stance Detection: Refugee Crisis")
        st.header("Welcome to our study!")
        st.subheader("Before proceeding to the annotation, it is strongly suggested that you go through the examples by clicking :green[**examples & introdcution**] in the sidebar to the left to get yourself familiar with the interface and the expected answers. You can also refer to it when you annotate.")
        st.subheader("Your answer is automatically saved when you proceed to the next instance. You can exit the survey at anytime and resume to your lastly finished instance by clicking the :green[jump to latest] button.")
        st.subheader("Please contact us on prolific immediately if you encounter any bugs.")
        st.subheader("Before you start, please read the following instructions:")
        display()
    def construct_annotations(self,cur_idx:int,example_id:str,targets_json:dict):
        """
        Display the options. 
        """
        n_selected = 0 
        st.session_state["annos_completed"][cur_idx] = True
        for i,target_item in enumerate(targets_json):

            target = target_item["target"]
            fg_target = target_item["fg_target"]
            target_disply = TARGETS_MAP.get(target,target)
            fg_target_disply = TARGETS_MAP.get(fg_target,fg_target)
            st.subheader(f"target pair {i+1}/{len(targets_json)}: {target_disply} - {fg_target_disply}",divider="red")
            l_col,m_col,r_col = st.columns(3)
            with l_col:
                st.subheader("target: ")
                st.write(f"Please choose how relevant the following target is toward the tweet: :red[{target_disply}]")             
                relevance = self.survey.radio("Relevance:",options=RELEVANT_CHOICES,horizontal=True,id=f"r_{target}_{example_id}",index=None)  
            if relevance and relevance != "irrelevant":
                with m_col:
                    if relevance:
                        index_prev = RELEVANT_CHOICES.index(relevance)
                    else:
                        index_prev = None
                    st.subheader("fine-grained target: ")
                    st.write(f"Please choose the stance of the tweet towards the fine-grained target: :red[{fg_target_disply}]")
                    relevance_fg = self.survey.radio("Relevance:",options=RELEVANT_CHOICES,id=f"rft_{target}_{example_id}",index=None if fg_target != target else index_prev,disabled=(fg_target == target)) 
                with r_col:
                    target_stance = fg_target if relevance_fg != "irrelevant" else target
                    st.subheader("stance: ")
                    st.write(f"Please choose the stance of the tweet towards the target: :red[{target_stance}]")
                    stance = self.survey.radio("Stance:",options=STANCE_OPTIONS,id=f"st_{target}_{example_id}",index=None) 
            test = self.attention_test.get(example_id)
    
            if test and target == test["target"]:
             
                st.session_state["test_passed"][test["index"]] = (relevance != "irrelevant" and stance == test["stance"])
            if relevance == "irrelevant":
                n_selected += 1 
            elif relevance and relevance_fg == "irrelevant":
                n_selected += 1
            elif relevance and stance:
                n_selected += 1
        if n_selected < len(targets_json):
            st.session_state["annos_completed"][cur_idx] = False
            st.warning("Please select the relevance and stance for all targets before proceeding to the next instance.")
    def annotation_page(self,n:int):
        '''
        Display the annotation page. 
        '''
        cur_idx = n - 1 
        st.title(f"Annotation: {cur_idx + 1}/{self.n_annotation}")     
        anno_example = self.anno_data[cur_idx]
        targets_json = anno_example["target_items"]
    
        st.header("Please read the following tweet:",divider="red")
        header = st.container(border=True)
        with header:
            text = anno_example["fullText"]

            if self.lang not in ["English","multiling"]:
                show_translation = st.checkbox("Show English translation", value=False)
                if show_translation:
                    text = self.data_translated[anno_example["resourceId"]]["fullText"]
            st.markdown(f"""<div class='fixed-header'>{text}""", unsafe_allow_html=True)
            st.markdown(TEXT_CSS,unsafe_allow_html=True)
        st.write(TASK_DESCRIPTION_STANCE)
        self.construct_annotations(cur_idx,anno_example["resourceId"],targets_json)
        self.pages.proceed_to_next = st.session_state["annos_completed"][cur_idx] if self.prolific_id != "default_prolific_id" else True # allow the coder to proceed to the next page if the prolific_id is default

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
        if difficulty and time and other:
            self.pages.allow_submit = True
    def submit_func(self):
        if self.save_to_mongodb():
            completion_link = st.secrets["completion_link"]
            st.success(f"Submission and saving successful! Please click the [completion link]({completion_link}) so that your work will be marked as completed. We will manually check your annotation and reward you accordingly.")  
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
    examples = st.Page(page="stranicy_stance/examples.py",title="examples & instructions",icon="📖")
    pg = st.navigation([main_page,examples])
    pg.run()