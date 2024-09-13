import streamlit as st
import my_streamlit_survey as ss 
import re
from survey import all_targets,task_description
examples = [
{"text":"Poland, Czech Republic, and Hungary, I advise you to :red[resist the pressure of the EU] to import :red[migrants]. If you need even more motivation, just look at Germany and Sweden.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The author of the post supports the hard-line asylum policies of Poland, Czechia and Hungary while hinting at the severe consequences of taking up migrants like Germany and Sweden. Although the post only mentions migrants, given the background knowledge of the 2014 refugee crisis the migrants here are the refugees from the Middle East. So the fine-grained target should be refugee."},{"t":"European Union Institutions -> none","s":"against","explanation":"The phrase 'pressure of the EU' indicates, given enough background knowledge, that the EU pressured its member states to accommodate refugees during the refugee. In this case,  'EU' is not merely a place name but a political institution that enacts laws and makes political decisions. Since no specific EU institution name such as EU parliament is mentioned, a fine-grained target is not applicable in this case. Also, the author criticises EU for its policies."}]},
{"text":"To the delusional leftists, Obama, Merkel, the Canadian Prime Minister, Pope Francis, United Nations, and others they say nothing goes wrong even though there are ongoing terrorism problems due to the :red[refugees and illegal aliens] in the EU and other places.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The post directly mentions “refugee” and concerns the mass influx of non-EU migrants. Note: “EU institutions” is not a target here because the author merely indicates that the refugees are coming to the “EU”, but the EU here is a place where the issue takes place rather than a political agency."}]},
{"text":":green[Salvini refuses to bend, I love it]. Italy - Salvini :red[Refuses To Let 177 Migrants] :orange[Off Ship] Till EU Agrees To Take Them (Video) news","ans":[{"t":"migrants -> refugees","s":"against","explanation":"Salvini is a right-wing Italian politician holding anti-migrant opinions. The post supports his hard-line policies against refugees thus the post is against the refugees."},{"t":"refugee pathways -> Mediterranean crossing","s":"none","explanation":"The mentions refugees coming to the EU by boat through the Mediterranean Sea, while no further stance is expressed."},{"t":"migration policies -> Salvini","s":"favor","explanation":"The post stongly support the migration policy of Salvini."}]},
{"text":"The funny thing about :red[Brexit is that even the racists will be disappointed by it]. The UK is not going to expel 2 million :green[EU workers otherwise economy collapses]. & future immigration more likely to come from Africa/Asia as Europeans won’t want to come without guaranteed rights.","ans":[{"t":"migrants -> economic migrants","s":"favor","explanation":"The post primarily mentions migrants and specifically concerns about the economic consequences of EU migrants leaving UK and acknowledges their contributions to the UK economy. Thus, the post talks about economic migrants from EU/Africa/Asia who come to the UK for career perspectives."},{"t":"migration policies -> UK","s":"against","explanation":"The post critizes the economic consequences of Brexit."}]},
{"text":"(translated from German)RT @warum_nur74 @Beatrix_vStorch The EU (SPD HrTönnes) wants to do it that way too. :green[Suspend Dublin] and then if a :red[refugee] in Libya says that his relative is in Germany, :orange[he comes straight to Germany. He doesn't need papers]. The word is enough. Sometimes I wish for other times.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The author wants a more tightened control of refugees, indicating a against stance toward refugees."},{"t":"migration policies -> Dublin Regulation","s":"favor","explanation":"The author of the post supports the Dublin Regulation that it regulates which refugee should be allocated to which EU country. Otherwise, the refugees will pick whatever country they like (especially wealthy EU country like Germany). (Migration Policies -> SPD -> against is an alternative answer.)"},{"t":"asylum procedures -> none","s":"none","explanation":"The author talks about the way and procedures a refugee is allocated to the receiving country (either through the Dublin agreement or depending on their relatives in Germany). But there is no clear stance towards this topic."}]},
{"text":"(translated from German)RT @Beatrix_vStorch :red[Migrant distribution] minister Seehofer is failing because of the EU states. Unlike the minister, they are still in their right minds. 110,000 asylum applications in Germany and he wants to take in even more. :red[Dear CSU, send him into retirement at last]. #AfD","ans":[{"t":"migrants -> asylum seekers","s":"against","explanation":"The author doesn’t want more asylum seekers in Germany."},{"t":"migration policies -> CSU","s":"against","explanation":"The post critizes the migration policy of CSU (AFD -> favor is also an acceptable answer)."}]}
]

def construct_annotations(cur_idx,example:dict):
     
    st.write(task_description)
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
            st.subheader(example["text"],divider="orange")
            l_col,r_col = st.columns([2,1])
            with l_col: 
                t_exist = st.radio(f"Does target :red[{t}] exist in the post?",options=["No","Yes"],horizontal=True,key=f"e_{t}_{cur_idx}",help=all_targets[t]["help"])
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
    st.header("Please read the example, answers and explanation below.",divider="red")
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
  
        st.subheader("Please choose the correct options based on the above answers.",divider="red")
        st.write("hint: You do not need to complete every instance as long as you are familiar with the interface.")
    

        construct_annotations(cur_idx,example)

def run():

    survey = ss.StreamlitSurvey("examples")
 
    pages = survey.pages(len(examples),progress_bar=True)
 
    with pages:
        example_page(pages.current,examples) 

if __name__ == "__main__":

    st.set_page_config(layout="wide")
    run()