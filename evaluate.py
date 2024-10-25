import streamlit as st 
import my_streamlit_survey as ss
from utils import *
RATING_SCALE = {"crap":0,"bad":1,"ok":2,"good":3,"excellent":4}
class EvalSurvey():
    def __init__(self,path_to_anno:str) -> None:
        # path example: anno_results/en/66c8690ad6fdb4de5a2102be.json 
        self.lang_id = path_to_anno.split("/")[1]
        self.id = path_to_anno.split("/")[2].split(".")[0]
        new_session = self.new_session()      
        res_dir = "eval_results"
        os.makedirs(res_dir,exist_ok=True)
        self.data_anno = load_anno_result(self.id,self.lang_id,new_session,path="anno_results")
        if not self.data_anno:
            st.error("No data found for this language and id")
        if new_session:
            self.data_res = load_anno_result(self.id,self.lang_id,new_session,path=res_dir)
            self.survey = ss.StreamlitSurvey("evaluation",data=self.data_res)
        self.survey = ss.StreamlitSurvey("evaluation")
        self.pages = self.survey.pages(len(self.data_anno),progress_bar=True,on_submit=self.save)
        # put completion and score status to session state if it is not present.
        self.pages.latest_page = 3

    def new_session(self):
        """
        Save the query parameters to session state for reuse.
        return :new_session. If it is a new session or not  
        """
 
        return len(st.session_state) == 0   
    def save(self):

        dir = f"eval_results/{self.lang_id}"
        os.makedirs(dir,exist_ok=True) 
        path = os.path.join(dir,self.id) + ".json"
        self.survey.to_json(path)
        st.success("Data saved successfully")
    def eval_page(self,page_idx):
        """
        Display the evaluation page for the given page index. 
        set the passed status for the given page index to true if the user has passed the evaluation.  
        """
        results = self.data_anno
        cur_example_id = list(results.keys())[page_idx]
        text = get_text_by_id(cur_example_id,self.lang_id)
        annos = self.data_anno[cur_example_id]
        
        
        
        col_l,col_m,col_r = st.columns(3)
        with col_l:
            st.subheader(f"Example {page_idx+1}/{len(results)}")
        with col_m:
            st.subheader(f"example id: {cur_example_id}")
        with col_r:
            st.subheader(f"prolific_id: {self.id}")
        
        with st.container(border=True):
            st.header(text)
        for anno in annos:
            target = anno["target"]
            fg_target = anno["fg_target"]
            stance = anno["stance"]
            with st.container(border=True):
                st.write(f"target: {target}")
                st.write(f"fg target: {fg_target}")
                st.write(f"stance: {stance}") 
        pass_btn = self.survey.radio(label="how do you like it?",options=RATING_SCALE.keys(),id=cur_example_id,horizontal=True,index=2)
        total_score = sum([RATING_SCALE[self.survey.data[id]["value"]] for id in self.survey.data.keys()])
        st.write(f"Total score: {total_score} / {len(self.data_anno) * 4}")
        self.save()


        
    def run(self):
        """
        Main function to launch the evaluation interface 
        True"""

        with self.pages:

            self.eval_page(self.pages.current)
      



    

if __name__ == "__main__":
    eval = EvalSurvey("anno_results/pl/5f1b1f4bcd241009e68d764c.json") 
    eval.run()