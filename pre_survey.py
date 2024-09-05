import streamlit as st 
from survey import * 
eligibility = True 
st.title("Pre-annotation survey")
st.header("Before procereding to the actual annotation. We could like you to answer a few questions to test your eligibility to participate.")

lang = st.selectbox("please choose your native language",options=lang2id.keys(),horizontal=True)
en_proficiency = st.selectbox("what is your English proficiency",options=["beginner","intermediate","advanced","native"],horizontal=True)
if en_proficiency == "beginner":
    eligibility = False 

