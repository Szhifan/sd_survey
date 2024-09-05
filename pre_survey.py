import streamlit as st 
from survey import * 
eligibility = True 
survey_link = ""
st.set_page_config(layout="wide")
st.title("Pre-annotation survey")
st.header("Before proceeding to the actual annotation. We would like to assess your ability to perform target and stance annotation on tweets about migrants by performing this task on simpler tweets with simpler question settings, good luck!")

st.write("Please check the sidebare for explanations and get yourself familiar withe the annotation interface!")
st.write("Please choose the fine-grained target (if applicable) and the corresponding stance in the following tweets.")


