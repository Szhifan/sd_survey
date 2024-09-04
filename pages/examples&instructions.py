import streamlit as st
import streamlit_survey as ss 
import json
from survey import all_targets 
@st.cache_data()
def load_data(path="examples.json"):
    with open(path,"r") as f:
        js = json.load(f)
    return js 

def construct_annotations(cur_idx,example:dict):
     
    st.write("please determine if the following targets appear in the post, the question mark contains the definition of the target that might be helpful to you. Once you have selected a target, please determine its fine-grained target (if available) and the stance. You can choose up to **three** targets")
    n_selected_trgt = 0 
    targets = all_targets.keys()
    ans_dict = {a["t"]:a["s"] for a in example["ans"]}
    # random.shuffle(list(targets))
    for t in targets:
        with st.container(border=True):
            l_col,r_col = st.columns([2,1])
            with l_col: 
                st.subheader(f"{t}",help=all_targets[t]["help"])
                t_selected = st.radio("please choose a fine-grained target (if applicable)", options=["NA"] + all_targets[t]["fg_targets"], horizontal=True,key = f"t_{t}_{cur_idx}")

                if t_selected != "NA":
                    n_selected_trgt += 1 
                    if t_selected not in ans_dict.keys():
                        st.error("please try again!")
                    else:
                        st.success("correct")
            with r_col:
                if t_selected != "NA" and t_selected in ans_dict.keys():
                    s_selected = st.radio(f"stance toward _{t_selected}_", options=["NA"] + ["favor", "against","none"], horizontal=True,key = f"s_{t}_{cur_idx}",help="please choose none if the post doesn't express a clear stance toward the topic.")
            
                    if s_selected == "NA":
                        st.warning("please choose a stance")
                    else:
                        if s_selected != ans_dict[t_selected]:
                            st.error("please try again!")
                        else:
                            st.success("correct!")
                    
    if not n_selected_trgt:
    
        st.warning("please choose at leat one target")
    if n_selected_trgt > 3:
        st.warning("you can only choose up to three targets")  

def example_page(cur_idx:int,data:list):
    
    example = data[cur_idx]
    st.title(f"Example and Instructions")
    st.write(f"{cur_idx+1}|{len(data)}")
    st.header("Please read the example, answers and explanation below.",divider="red")

    with st.container(border=True):
        st.subheader(example["text"])
   
    with st.container():
        st.subheader("Answers  & explanation",divider="red")
        for i,ans in enumerate(example["ans"]):
            st.write(f"answer {i+1}")
            l_col,m_col,r_col = st.columns([2,1,3])
            with l_col:
                t = ans["t"]
                st.write(f"**(fine-grained) target**: {t}")
            with m_col:
                s = ans["s"]
                if s == "against":
                    color = "red"
                elif s == "favor":
                    color = "green"
                elif s == "none":
                    color = "blue"
                st.write(f"**stance**: :{color}[{s}]")
            with r_col:
                ex = ans["explanation"]
                st.write(f"**explanation**: {ex}")

    with st.container():
        st.subheader("Please choose the correct options based on the above answers.",divider="red")
        st.write("hint: you do not need to complete every instance as long as you are familiar with the interface")
        construct_annotations(cur_idx,example)

def run():

    survey = ss.StreamlitSurvey("examples")
    data = load_data()
    pages = survey.pages(len(data),progress_bar=True)
 
    with pages:
        example_page(pages.current,data) 

if __name__ == "__main__":
    run()