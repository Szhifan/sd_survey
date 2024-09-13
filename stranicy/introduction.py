import streamlit as st 

st.title("Introduction")
st.header("Task Introduction",divider="red")
st.write("""This study aims to obtain human annotation for a Stance Detection (SD) dataset, consisting mainly of tweets on the topic of the migration crisis across Europe between 2014 and 2019. By annotating the tweets, we wish to study the attitudes of EU citizens toward migrants/refugees and how the EU governments managed the refugee crisis. 
An SD example typically involves **target(s)**, **stance(s)**, and a piece of text, where a **stance** (support, oppose, neutral, etc.) is expressed toward a target in this piece of text. Our dataset differs from other SD datasets in that the target is divided into broad and fine-grained targets. A fine-grained target is often the hyponym of a broad target. For instance, "refugee" and "economic migrants" are the fine-grained targets under "migrants". 
""")

st.header("Task Description",divider="red")
st.write(""" In this study, you will annotate the broad and fine-grained targets and their corresponding stance for 100 tweets (you can exit and re-enter the interface if you wish to pause, and your results will be saved). 
Given a tweet, you have to identify 1) If one or multiple broad targets exist, 2) if the tweet further mentions a fine-grained target within the broad target, and 3) what is the stance of the tweets toward the selected targets.  Before proceeding to the actual annotation, we will test your ability by performing the SD annotation on a few simpler examples, you will proceed to the actual annotation if your performance is satisfactory. 
""")
st.header("Background Information",divider="red")
