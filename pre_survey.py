import streamlit as st  
import json 
import streamlit_survey as ss 
from urllib.parse import urlencode
survey_link = ""
st.set_page_config(layout="wide")
targets =  {
    "migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",],"help":None},
    "European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"],"help":"FRONTEX:European Border and Coast Guard Agency;ECHO:European Civil Protection and Humanitarian Aid Operations"}}
def questions(survey:ss.StreamlitSurvey):

    score = 0  
    with open("pre_test.json","r") as f:
        data = json.load(f)  
    for i,item in enumerate(data):
        with st.container(border=True):
            text = item["text"]
            st.subheader(f"{i+1}: {text}",divider="red")
            n_t_selected = 0 
            for t in targets:
                l_col,r_col = st.columns([2,1])
                with l_col:
                    st.subheader(f"{t}",help=targets[t]["help"]) 
                    t_selected = survey.radio("please choose a fine-grained target, choose 'none' (if applicable) if only broad target exists.",options=["No selection"] + targets[t]["fg_targets"],horizontal=True,id=f"t_{t}_{i}")
                    if t_selected != "No selection":
                        n_t_selected += 1
                    if t_selected == "none":
                        t_selected = t
                     
                    
                with r_col:
                    if t_selected!="No selection":
                        s_selected = survey.radio(f"stance toward _{t_selected}_", options=["No selection"] + ["favor", "against","none"], horizontal=True,id = f"s_{t}_{i}",help="please choose none if the post doesn't express a clear stance toward the topic.")
                        if s_selected == "No selection":
                            st.warning("please choose a stance.")
           

                if t_selected in item["target"] and s_selected in item["stance"]:
                    score += 1 
          
            if not n_t_selected:
                st.warning("please choose at least one target.")
    return score 

def set_qp():
    
    if "qp" not in st.session_state:
        st.session_state["qp"] = st.query_params.to_dict()  
    if not len(st.session_state["qp"]):
        st.session_state["qp"]["LANG"] = "English"
        st.session_state["qp"]["PROLIFIC_PID"] =  "default_prolific_id"  
        st.session_state["qp"]["STUDY_ID"]  = "default_study_id"
    
    st.query_params.from_dict(st.session_state["qp"])           
def main():
    survey_link = f"https://sdsurvey-ew4vwqofwonjaw6ojqrmd2.streamlit.app/?"
    set_qp()
    survey = ss.StreamlitSurvey("sd annotation: pre-survey")
    st.title("Pre-annotation survey")
    st.header("Before proceeding to the actual annotation. We would like to assess your ability to perform target and stance annotation on tweets about migrants by annotating target and stance on simpler tweets with simpler question settings, good luck!",divider="red")

    st.write("Please check the sidebare for explanations and get yourself familiar withe the annotation interface!")
    st.write("please determine if the following targets appear in these posts, the question mark contains the definition of the target that might be helpful to you. Once you have selected a target, please determine its fine-grained target (if available) and the stance.")
    
    score = questions(survey)
    params = urlencode(st.session_state["qp"]) 
    btn = st.button("finish and submit")
    if btn:
        if score >= 3:
            st.success(f"Congradulations, you have passed the test, please click this [link]({survey_link + params}) for the actual annotation.")
        else:
            st.error("sorry, you didn't past the test.")




if __name__ == "__main__":
    main()