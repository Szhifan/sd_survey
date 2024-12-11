import streamlit as st
import my_streamlit_survey as ss 
import re
from utils import * 

from interface_utils import ALL_TARGETS,TASK_DESCRIPTION_STANCE,TEXT_CSS,EXAMPLES,RELEVANT_CHOICES,STANCE_OPTIONS


def construct_annotations(cur_idx,example:dict): 
    n_selected = 0 
    target_objs = example["ans_stance"]

    for i,target_obj in enumerate(target_objs):
        target,fg_target = target_obj["t"].split(" -> ")
        st.subheader(f"target pair {i+1}|{len(target_objs)}: {target} - {fg_target}",divider="red")
        ans_relevance,ans_fg_relevance = target_obj["r"].split(" -> ")
        ans_stance = target_obj.get("s")
        l_col,m_col,r_col = st.columns([1,1,1])
        with l_col:
            st.subheader("target: ")
            st.write(f"Please choose how relevant the target is toward the tweet: :red[{target}]")
            relevance = st.radio("Relevance:", options=RELEVANT_CHOICES, horizontal=True, key=f"r_{target}_{cur_idx}", index=None)

            if relevance and relevance != ans_relevance:
                st.error("please try again")
            elif relevance and relevance == ans_relevance:
                st.success("correct")
        if relevance and relevance != "irrelevant":
            with m_col:
                st.subheader("fine-grained target: ")
                st.write(f"Please choose the stance of the tweet towards the fine-grained target: :red[{fg_target}]")
                relevance_fg = st.radio("Relevance:", options=RELEVANT_CHOICES, key=f"rft_{target}_{cur_idx}", index=None if fg_target != target else RELEVANT_CHOICES.index(relevance), disabled=(fg_target == target))
                if relevance_fg and relevance_fg != ans_fg_relevance:
                    st.error("please try again")
                elif relevance_fg and relevance_fg == ans_fg_relevance:
                    st.success("correct")
            with r_col:
                target_stance = fg_target if relevance_fg != "irrelevant" else target
                st.subheader("stance: ")
                st.write(f"Please choose the stance of the tweet towards the target: :red[{target_stance}]")
                stance = st.radio("Stance:", options=STANCE_OPTIONS, key=f"st_{target}_{cur_idx}", index=None)
                if stance and stance != ans_stance:
                    st.error("please try again")
                elif stance and stance == ans_stance:
                    st.success("correct")
        if relevance == "irrelevant":
            n_selected += 1
        elif relevance and relevance_fg == "irrelevant":
            n_selected += 1
        elif relevance and stance:
            n_selected += 1
    if n_selected < len(target_objs):
        st.warning("Please select the relevance and stance for all targets before proceeding to the next instance.")
def example_page(cur_idx:int,data:list):
    
    example = data[cur_idx]
    st.title(f"Example and Instructions")
    st.header("Interface Introduction",divider="red")
    st.write("""
    The coding interface is designed in a three-step process.
    For each post, you will be presented some target - fine-grained target pairs selected by the LLM.
    \n **Step 1**: Choose how relevant the target is w.r.t the post. If you choose "irrelevant", you do not need to complete the next steps.
    \n **Step 2**: If the target is not irrelevant, choose how relevant the fine-grained target is w.r.t the post. 
    \n **Step 3**: If the fine-grained target is not irrelevant, choose the stance of the post towards the fine-grained target. In case the fine-grained target is irrelevant but the target is relevant, you will be asked to choose the stance of the target.
            """)
    
             
    st.header("Please read the post, and select the correct answers given the explanations.",divider="red")
    st.write(f"{cur_idx+1}/{len(data)}")
    header = st.container(border=True)
    with header:
        text = example["text"]
        st.markdown(f"""<div class='fixed-header'>{text}""", unsafe_allow_html=True)
        st.markdown(TEXT_CSS,unsafe_allow_html=True)
    lc,rc = st.columns([1,2],vertical_alignment="top")
    with lc:
        st.subheader("Answer and explanation",divider="red")
    
        with st.container(border=True):
            for i,ans in enumerate(example["ans_stance"]):
                st.subheader(f"target pair {i+1}",divider="red")

                l_col,r_col = st.columns([1,1])
                with l_col:
                    t,fgt = ans["t"].split("->")
                    st.write(f"**target -> fine-grained target**:")
                    st.write(f"{t} -> {fgt}")
                    r = ans["r"]
                    st.write(f"**relevance**: ")
                    st.write(r)
                    s = ans.get("s")
                    if s:
                        st.write(f"**stance**: ")
                        if s == "negative":
                            color = "red"
                        elif s == "positive":
                            color = "green"
                        elif s == "neutral":
                            color = "orange"
                        else: 
                            color = "white"
                        st.write(f":{color}[{s}]")
                with r_col:
                    ex = ans["explanation"]
                    st.write(f"**explanation**: {ex}")
            
        
    with rc:
        st.subheader("Please choose the correct options based on the answers and explanations.",divider="red")
        st.write("hint: You do not need to complete every instance as long as you are familiar with the interface.")
        st.write(TASK_DESCRIPTION_STANCE)
        construct_annotations(cur_idx,example)
 

def main():
    survey = ss.StreamlitSurvey("examples")
    pages = survey.pages(len(EXAMPLES),progress_bar=True)
    with pages:
        example_page(pages.current,EXAMPLES) 

main()