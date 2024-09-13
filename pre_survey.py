import streamlit as st  
import my_streamlit_survey as ss 
from survey import load_results 

from urllib.parse import urlencode
survey_link = f"https://sdsurvey-mhermhvefcfupvcnif5swf.streamlit.app/?"
pre_tests = [
            {"text":"RT @trevdick Farage claims to be uncomfortable with EU migrants not learning English, my exp tells me many more of them speak English than Brits abroad!>","target":["migrants","economic migrants"],"stance":["favor"]},
            {"text":"let the russians have ukraine, if they joined the eu england would have to put up with another million immigrants to give jobs+homes to","target":["migrants","economic migrants"],"stance":["against"]},
            {"text":"#Disaster #humanity European Commission Pledges 3.9 Million Euro in Aid to Kobani Refugees - RIA ... http://t.co/isnrtULyBL #HumanRights","target":["European Commission","refugees"],"stance":["favor","none"]}, 
            {"text":"@DrGertJanMulder: Are you fond of English as I do: EU asylum plan presents a threat to our civilisation -UKIP leader Nigel","target":["asylum seekers", "refugees"],"stance":"against"}]
st.set_page_config(layout="wide")
targets =  {
    "migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",],"help":None},
    "European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"],"help":"FRONTEX:European Border and Coast Guard Agency;ECHO:European Civil Protection and Humanitarian Aid Operations"}}
def questions(survey:ss.StreamlitSurvey):

    score = 0  

    for i,item in enumerate(pre_tests):
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
                        s_selected = survey.radio(f"stance toward _{t_selected}_", options=["No selection"] + ["favor", "against","none"], horizontal=True,id = f"s_{t}_{i}")
                        if s_selected == "No selection":
                            st.warning("please choose a stance.")
                if t_selected in item["target"] and s_selected in item["stance"]:
                    score += 1 
          
            if not n_t_selected:
                st.warning("please choose at least one target.")
    return score 
def get_survey_url(params:dict):
    parsed_params = urlencode(params)
    return survey_link + parsed_params
def set_qp():
    
    if "qp" not in st.session_state:
        st.session_state["qp"] = st.query_params.to_dict()  
    if not len(st.session_state["qp"]):
        st.session_state["qp"]["LANG"] = "English"
        st.session_state["qp"]["PROLIFIC_PID"] =  "default_prolific_id"  
        st.session_state["qp"]["STUDY_ID"]  = "default_study_id"
    
    st.query_params.from_dict(st.session_state["qp"])           
def main():
    set_qp()
    used_data = load_results(lang=st.session_state["qp"]["LANG"],id=st.session_state["qp"]["PROLIFIC_PID"])
    anno_url = get_survey_url(st.session_state["qp"])
    if used_data:

        st.success(f"You have passed the test, please click this [link]({anno_url}) to proceed to the annotation.")
        return 
    survey = ss.StreamlitSurvey("sd annotation: pre-survey")
    st.title("Pre-annotation survey")
    st.header("Before proceeding to the actual annotation. We would like to assess your ability to perform target and stance annotation on simpler tweets with simpler question settings, good luck!",divider="red")
    st.write("Please check the sidebar for explanations and get yourself familiar with the annotation interface first.")
    st.write("Please determine if the following targets appear in the post, the **question mark** contains the definition of the target that might be helpful to you. Once you have selected a target, please determine its fine-grained target (choose **none** if no fine-grained target applies) and the stance (choose **none** if there is no clear stance toward the target). To cancel your selection, please click **No selection**.")
    
    score = questions(survey)
    btn = st.button("finish and submit")
    if btn:
        if score >= 3:
            st.success(f"Congratulations, you have passed the test, please click this [link]({anno_url}) to proceed to the annotation")
        else:
            st.error("Sorry, you didn't pass the test.")
if __name__ == "__main__":
    main()