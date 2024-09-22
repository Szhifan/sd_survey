import streamlit as st
import my_streamlit_survey as ss 
import re
from utils import * 


def construct_annotations(cur_idx,example:dict): 
    n_selected_trgt = 0 
    targets = all_targets.keys()
    open_end_mg = None 
    ans_bt = {a["t"].split("->")[0].strip():a["s"] for a in example["ans"]}
    ans_fgt = {a["t"].split("->")[1].strip():a["s"] for a in example["ans"]}
    bt_fgb = {a["t"].split("->")[0].strip():a["t"].split("->")[1].strip() for a in example["ans"]}

    if "migration policies" in ans_bt.keys() and bt_fgb["migration policies"] not in all_targets["migration policies"]["fg_targets"]:
        open_end_mg = bt_fgb["migration policies"]

    # random.shuffle(list(targets))
    for t in targets:
        with st.container(border=True):

            l_col,r_col = st.columns([2,1])
            with l_col: 
                t_exist = st.radio(f"Does target :red[{t}] exist in the post?",options=["No","Yes"],horizontal=True,key=f"e_{t}_{cur_idx}")
                if t_exist == "No":
                    continue 
                if t_exist == "Yes" and t not in ans_bt.keys():
                    st.error("Please choose the correct target.")
                    continue

                n_selected_trgt += 1
                t_selected = st.radio("Please choose a fine-grained target, choose **none** (if applicable) if only broad target exists.", options=all_targets[t]["fg_targets"], horizontal=True,key = f"t_{t}_{cur_idx}",index=None)
                if t == "migration policies" and t_selected and t_selected.startswith("poli"):
                    t_selected = st.text_input("What political entity does the post mention? (Please only answer with the entity name.)",key = f"mp_{t}_{cur_idx}",placeholder="plase enter: " + open_end_mg)
                    if not t_selected:
                        st.warning("Please provide a political entity name and press enter.")            
            with r_col:
       
                if t_selected:
                    s_selected = st.radio(f"stance toward _{t_selected}_", options=["favor", "against","none"], horizontal=True,key = f"s_{t}_{cur_idx}",index=None)

                    if not s_selected:
                        st.warning("please choose a stance")
                    else:
                        if t_selected in ans_fgt and ans_fgt[t_selected] == s_selected:
                            st.success("Correct")
                        else:
                            st.error("Incorrect")
                        
    if not n_selected_trgt:

        st.warning("please choose at leat one target")
    if n_selected_trgt > 3:
        st.warning("you can only choose up to three targets")  

def example_page(cur_idx:int,data:list):
    
    example = data[cur_idx]
    st.title(f"Example and Instructions")
    st.write(f"{cur_idx+1}|{len(data)}")
    st.header("Please read the post, answers, and explanation.",divider="red")
    header = st.container(border=True)
    header.subheader(example["text"],divider="red")
    header.markdown(text_css,unsafe_allow_html=True)
    header.write(task_description)
    lc,rc = st.columns([1,2],vertical_alignment="top")
    with lc:
        st.subheader("Answer and explanation",divider="red")
    
   
        with st.container(border=True):
     
            for i,ans in enumerate(example["ans"]):
                st.subheader(f"answer {i+1}")
                l_col,m_col,r_col = st.columns([2,1,3])
                with l_col:
                    t = ans["t"]
                    st.write(f"**target**:")
                    st.write(f"_{t}_")
                with m_col:
                    s = ans["s"]
                    if s == "against":
                        color = "red"
                    elif s == "favor":
                        color = "green"
                    elif s == "none":
                        color = "orange"
                    else: 
                        color = "white"
                    st.write(f"**stance**: :{color}[{s}]")
                with r_col:
                    ex = ans["explanation"]
                    st.write(f"**explanation**: {ex}")
                if t.startswith("migration policies of"):
                    st.write("Hint: For this target, you should choose **policies of a political entity (party, country or politician)** under **migration policies**, and then enter the corresponding entity name.")
        
    with rc:
        st.subheader("Please choose the correct options based on the answers and explanations.",divider="red")
        st.write("hint: You do not need to complete every instance as long as you are familiar with the interface.")

        construct_annotations(cur_idx,example)
 

def main():

    survey = ss.StreamlitSurvey("examples")
 
    pages = survey.pages(len(examples),progress_bar=True)
 
    with pages:
        example_page(pages.current,examples) 

main()