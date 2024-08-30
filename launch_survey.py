import streamlit as st
import streamlit_survey as ss 


class SDSurvey: 
    def __init__(self) -> None:
        self.success = False 
        self.survey = ss.StreamlitSurvey("sd annotation survey")
        self.data = dict()
        self.pages = self.survey.pages(5,progress_bar=True,on_submit=self.submit_func)
    def submit_func(self):
        if self.success:
            st.success("Submitted!")
        else:
            st.error("submission failed")
    