import streamlit as st  
import my_streamlit_survey as ss 
from survey import load_results 
from utils import ALL_TARGETS,task_description
from urllib.parse import urlencode
survey_link = f"https://sdsurvey-actazgy67pazw8zrtg9mx4.streamlit.app/?"
pre_tests = [
            {"text":"RT @trevdick Farage claims to be uncomfortable with EU migrants not learning English, my exp tells me many more of them speak English than Brits abroad!>","target":["migrants","economic migrants"],"stance":["favor"]},
            {"text":"let the russians have ukraine, if they joined the eu england would have to put up with another million immigrants to give jobs+homes to","target":["migrants","economic migrants"],"stance":["against"]},
            {"text":"#Disaster #humanity European Commission Pledges 3.9 Million Euro in Aid to Kobani Refugees - RIA ... http://t.co/isnrtULyBL #HumanRights","target":["European Commission","refugees"],"stance":["favor","none"]}, 
            {"text":"@DrGertJanMulder: Are you fond of English as I do: EU asylum plan presents a threat to our civilisation -UKIP leader Nigel","target":["asylum seekers", "refugees","European Union Institutions"],"stance":["against"]}]
st.set_page_config(layout="wide")
pre_tests_targets =  {
    "migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",],"help":None},
    "European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"],"help":"FRONTEX:European Border and Coast Guard Agency;ECHO:European Civil Protection and Humanitarian Aid Operations"}}

def questions(survey:ss.StreamlitSurvey):
    score = 0  

    for i,item in enumerate(pre_tests):
        with st.container(border=True):
            text = item["text"]
            st.subheader(f"{i+1}: {text}",divider="red")
            n_t_selected = 0 
            st.write(task_description)

            for t in pre_tests_targets:
                l_col,r_col = st.columns([2,1])
                with l_col:
                    fg_targets = " | ".join(ALL_TARGETS[t]["fg_targets"])
                    t_exist = survey.radio(f"Does target :red[{t}] exist in the post?",options=["No","Yes"],horizontal=True,id=f"e_{t}_{i}",help=fg_targets)
                    if t_exist == "No":
                        continue 
                    n_t_selected += 1
                    t_selected = survey.radio("please choose a fine-grained target, choose 'none' (if applicable) if only broad target exists.",options = pre_tests_targets[t]["fg_targets"],id=f"t_{t}_{i}",horizontal=True,index=None)
                  
                    if t_selected == "none":
                         t_selected = t 
            
                if t_selected:
                        
                    with r_col:
                        if t_selected!="No selection":
                            s_selected = survey.radio(f"stance toward _{t_selected}_", options=["favor", "against","none"], horizontal=True,id = f"s_{t}_{i}",index=None)
                            if not s_selected:
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
    st.header("Thank you for your interest in taking part in our study! Before proceeding to the actual annotation. We would like to assess your ability to perform target and stance annotation on simpler tweets with simpler question settings, good luck!",divider="red")
    st.write("Please click :green[**introduction**] in the sidebar for more background information and the domain knowledge of this task.") 
    st.write("Before starting the test, it is strongly suggested that you go through the examples by clicking the sidebar :green[**examples&instruction**] in the sidebar to the left to get yourself familiar with the interface and the expected answers.")
    st.write("You can always refer to the sidebar for the examples and instructions.") 
    st.write("The question mark icon on next to each question provides you with the fine-grained targets that you can choose from.")
    st.write("Please contact us on prolific if you encounter any issues or have any questions.")
    score = questions(survey)
    btn = st.button("finish and submit")
    if btn:
        if score >= 3:
            st.success(f"Congratulations, you have passed the test, please click this [link]({anno_url}) to proceed to the annotation")
        else:
            st.error("Sorry, you didn't pass the test.")
if __name__ == "__main__":
    
    main_page = st.Page(page=main,title="Pre-annotation survey",icon=":material/assignment_turned_in:")
    instructions = st.Page(page="stranicy/introduction.py",title="introduction",icon="💡")
    examples = st.Page(page="stranicy/examples.py",title="examples & instructions",icon="📖")
    pg = st.navigation([main_page,instructions,examples])
    pg.run()