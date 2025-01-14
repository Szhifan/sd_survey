import streamlit as st

def display():
    st.title("Introduction")
    st.header("Task Description",divider="red")
    st.write("**Stance Detection**")
    st.write("""
    Stance Detection (SD) is the task of determining the attitude expressed in a text towards a target. The most important components of a SD dataset are the target and the stance. The target is the entity towards which the attitude is expressed, and the stance is the attitude itself.
    In our study, we focus on the stance detection of social media posts towards migrants. You will be presented with a pair of targets, where the first on is migrant and the second one is the 
    specific type of migrants, e.g., refugees, asylum seekers, etc. Your task is to determine the stance of the tweet towards the target. The stance can be one of the following:
    - :green[**positive**]: the tweet expresses a welcoming attitude or show sympathy towards the migrants during the refugee crisis. 
    - :red[**negative**]: the tweet expresses a hostile attitude or show lack of symphathy towards the migrants during the refugee crisis.
    - :orange[**neutral**]: the tweet does not express any attitude towards the migrants during the refugee crisis. Or the stance cannot be determined from the given text.
    """) 