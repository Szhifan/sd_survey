import streamlit as st
import my_streamlit_survey as ss 
import json
from survey import all_targets 
examples = [
{"text":"Poland, Czech Republic, and Hungary, I advise you to :red[resist the pressure of the EU] to import :red[migrants]. If you need even more motivation, just look at Germany and Sweden.","ans":[{"t":"refugees","s":"against","explanation":"The author of the post supports the hard-line asylum policies of Poland, Czechia and Hungary while hinting at the severe consequences of taking up migrants like Germany and Sweden. Although the post only mentions migrants, given the background knowledge of the 2014 refugee crisis the migrants here are the refugees from the Middle East. So the fine-grained target should be refugee."},{"t":"European Union Institutions","s":"against","explanation":"The phrase 'pressure of the EU' indicates, given enough background knowledge, that the EU pressured its member states to accommodate refugees during the refugee. In this case,  'EU' is not merely a place name but a political institution that enacts laws and makes political decisions. Since no specific EU institution name such as EU parliament is mentioned, a fine-grained target is not applicable in this case. Also, the author criticises."}]},
{"text":"To the delusional leftists, Obama, Merkel, the Canadian Prime Minister, Pope Francis, United Nations, and others they say nothing goes wrong even though there are ongoing terrorism problems due to the :red[refugees and illegal aliens] in the EU and other places.","ans":[{"t":"refugees","s":"against","explanation":"The post directly mentions “refugee” and concerns the mass influx of non-EU migrants. Note: “EU institutions” is not a target here because the author merely indicates that the refugees are coming to the “EU”, but the EU here is a place where the issue takes place rather than a political agency."}]},
{"text":"Salvini refuses to bend, I love it. Italy - Salvini Refuses To Let 177 :red[Migrants Off Ship] Till EU Agrees To Take Them (Video) news","ans":[{"t":"refugees","s":"against","explanation":"Salvini is a right-wing Italian politician holding anti-migrant opinions. The post supports his hard-line policies against refugees thus the post is against the refugees."},{"t":"Mediterranean crossing","s":"none","explanation":"The mentions refugees coming to the EU by boat through the Mediterranean Sea, while no further stance is expressed."}]},
{"text":"The funny thing about Brexit is that even the racists will be disappointed by it. The UK is not going to expel 2 million :red[EU workers] otherwise economy collapses. & future immigration more likely to come from Africa/Asia as Europeans won’t want to come without guaranteed rights.","ans":[{"t":"economic migrants","s":"favor","explanation":"The post primarily mentions migrants and specifically concerns about the economic consequences of EU migrants leaving UK and acknowledges their contributions to the UK economy. Thus, the post talks about economic migrants from EU/Africa/Asia who come to the UK for career perspectives."}]},
{"text":"(translated from German)RT @warum_nur74 @Beatrix_vStorch The EU (SPD HrTönnes) wants to do it that way too. :red[Suspend Dublin] and then if a :red[refugee] in Libya says that his relative is in Germany, :red[he comes straight to Germany. He doesn't need papers]. The word is enough. Sometimes I wish for other times.","ans":[{"t":"refugees","s":"against","explanation":"The author wants a more tightened control of refugees, indicating a against stance toward refugees."},{"t":"Dublin Agreement","s":"favor","explanation":"The author of the post acknowledges the favor effects of the Dublin agreement that it regulates which refugee should be allocated to which EU country. Otherwise, the refugees will pick whatever country they like."},{"t":"asylum procedures","s":"none","explanation":"The author talks about the way and procedures a refugee is allocated to the receiving country (either through the Dublin agreement or depending on their relatives in Germany). But there is no clear stance towards this topic."}]},
{"text":"(translated from German)RT @Beatrix_vStorch :red[Migrant distribution] minister Seehofer is failing because of the EU states. Unlike the minister, they are still in their right minds. 110,000 :red[asylum applications] in Germany and he wants to take in even more. Dear CSU, send him into retirement at last. #AfD","ans":[{"t":"asylum seekers","s":"against","explanation":"The author doesn’t want more asylum seekers in Germany."},{"t":"refugee quotas","s":"against","explanation":" The author talks about migrant distribution, which is refugee quotas in this context and criticises that this policy is failing and that Germany cannot take more refugees."}]}
]

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
                t_selected = st.radio("please choose a fine-grained target, choose 'none' (if applicable) if only broad target exists.", options=["No selection"] + all_targets[t]["fg_targets"], horizontal=True,key = f"t_{t}_{cur_idx}")

                if t_selected != "No selection":
                    n_selected_trgt += 1 
                    if t_selected not in ans_dict.keys():
                        st.error("incorrect")
                    else:
                        st.success("correct")
            with r_col:
                if t_selected != "No selection" and t_selected in ans_dict.keys():
                    s_selected = st.radio(f"stance toward _{t_selected}_", options=["No selection"] + ["favor", "against","none"], horizontal=True,key = f"s_{t}_{cur_idx}",help="please choose none if the post doesn't express a clear stance toward the topic.")
            
                    if s_selected == "No selection":
                        st.warning("please choose a stance")
                    else:
                        if s_selected != ans_dict[t_selected]:
                            st.error("incorrect")
                        else:
                            st.success("correct")
                    
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
        
        bt = st.button("show options")
       
        construct_annotations(cur_idx,example)

def run():

    survey = ss.StreamlitSurvey("examples")
 
    pages = survey.pages(len(examples),progress_bar=True)
 
    with pages:
        example_page(pages.current,examples) 

if __name__ == "__main__":
    print(123)
    st.set_page_config(layout="wide")
    run()