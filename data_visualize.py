import streamlit as st 
import my_streamlit_survey as ss 
from utils import fetch_annotation,text_css
from collections import Counter
import json
def visualize_data(index,anno_data):

    item = anno_data[index]

    st.header(f"Resource ID: {item['resourceId']}")
    st.subheader(f"Agreement Score: {item['agreement_score']}")
    st.subheader(f"Text:",divider="red")
    header = st.container(border=True)
    with header:
        text = item["text"]
        st.markdown(f"""<div class='fixed-header'>{text}""", unsafe_allow_html=True)
        st.markdown(text_css,unsafe_allow_html=True)
    counter = {}
    col_1, col_2 = st.columns(2)
    with col_1:
        for coder_id, annotations in item.items():
            if coder_id not in ["resourceId", "agreement_score", "text"]:
                st.subheader(f"Coder ID: {coder_id}")
                st.write("Annotations:")
                for item in annotations:
                    if "fg_target" in item:
                        item["fine_grained_target"] = item.pop("fg_target")
                    st.write(item)
                    if item["fine_grained_target"] not in counter:
                        counter[item["fine_grained_target"]] = {"favor":0,"against":0,"none":0}
                    counter[item["fine_grained_target"]][item["stance"]] += 1
    with col_2:
        st.subheader("Summary")
        for target, stance in counter.items():
            st.write(f"Target: {target}")
            st.write(f"Stance: {stance}")
            st.write("----")
        


def dispaly(lang_id):
    anno_data_path = "all_anno_results/" + lang_id + ".json"
    with open(anno_data_path) as f:
        anno_data = json.load(f)

    survey = ss.StreamlitSurvey("display data")
    pages = survey.pages(len(anno_data),progress_bar=True,on_submit=None)
    with pages:
        visualize_data(pages.current,anno_data)

if __name__ == "__main__":

    dispaly("de")