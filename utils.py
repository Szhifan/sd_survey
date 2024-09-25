
import re 
import streamlit as st 
import json 
import os 
from pymongo.mongo_client import MongoClient
# from sklearn.metrics import cohen_kappa_score 
all_targets = {
"migration policies":{"fg_targets":["policies of a political entity (party, country or politician) or 'concret policy name' (e.g. Brexit)","EU-Turkey refugee return agreement","Dublin Regulation","Refugee Quotas"]},
"European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"]},
"refugee pathways":{"fg_targets":["none","boat sinking","Mediterranean crossing","smuggling"]},
"reception":{"fg_targets":["none","refugee camps","refugee status"]},
"asylum procedures":{"fg_targets":["none","protection", "compensation", "legal rights"]},
"migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",]}
} 
all_fg_targets = [item for target in all_targets.values() for item in target["fg_targets"]]
examples = [
{"text":"Poland, Czech Republic, and Hungary, I advise you to resist the pressure of the EU to import migrants. If you need even more motivation, just look at Germany and Sweden.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The author of the post supports the hard-line asylum policies of Poland, Czechia and Hungary while hinting at the severe consequences of taking up migrants like Germany and Sweden. Although the post only mentions migrants, given the background knowledge of the 2014 refugee crisis the migrants here are the refugees from the Middle East. So the fine-grained target should be refugee."},{"t":"European Union Institutions -> none","s":"against","explanation":"The phrase 'pressure of the EU' indicates, given enough background knowledge, that the EU pressured its member states to accommodate refugees during the refugee. In this case,  'EU' is not merely a place name but a political institution that enacts laws and makes political decisions. Since no specific EU institution name such as EU parliament is mentioned, a fine-grained target is not applicable in this case. Also, the author criticises EU for its policies."}]},
{"text":"Salvini refuses to bend, I love it. Italy - Salvini Refuses To Let 177 Migrants Off Ship Till EU Agrees To Take Them (Video) news","ans":[{"t":"migrants -> refugees","s":"against","explanation":"Salvini is a right-wing Italian politician holding anti-migrant opinions. The post supports his hard-line policies against refugees thus the post is against the refugees."},{"t":"refugee pathways -> Mediterranean crossing","s":"none","explanation":"The mentions refugees coming to the EU by boat through the Mediterranean Sea, while no further stance is expressed."},{"t":"migration policies -> Salvini","s":"favor","explanation":"The post stongly support the migration policy of Salvini."}]},
{"text":"The funny thing about Brexit is that even the racists will be disappointed by it. The UK is not going to expel 2 million EU workers otherwise economy collapses. & future immigration more likely to come from Africa/Asia as Europeans won’t want to come without guaranteed rights.","ans":[{"t":"migrants -> economic migrants","s":"favor","explanation":"The post primarily mentions migrants and specifically concerns about the economic consequences of EU migrants leaving UK and acknowledges their contributions to the UK economy. Thus, the post talks about economic migrants from EU/Africa/Asia who come to the UK for career perspectives."},{"t":"migration policies -> UK","s":"against","explanation":"The post critizes the economic consequences of Brexit."}]},
{"text":"(translated from German)RT @warum_nur74 @Beatrix_vStorch The EU (SPD HrTönnes) wants to do it that way too. Suspend Dublin and then if a refugee in Libya says that his relative is in Germany, he comes straight to Germany. He doesn't need papers. The word is enough. Sometimes I wish for other times.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The author wants a more tightened control of refugees, indicating a against stance toward refugees."},{"t":"migration policies -> Dublin Regulation","s":"favor","explanation":"The author of the post supports the Dublin Regulation that it regulates which refugee should be allocated to which EU country. Otherwise, the refugees will pick whatever country they like (especially wealthy EU country like Germany). (Migration Policies -> SPD -> against is an alternative answer.)"},{"t":"asylum procedures -> none","s":"none","explanation":"The author talks about the way and procedures a refugee is allocated to the receiving country (either through the Dublin agreement or depending on their relatives in Germany). But there is no clear stance towards this topic."}]},
{"text":"(translated from German)RT @Beatrix_vStorch Migrant distribution minister Seehofer is failing because of the EU states. Unlike the minister, they are still in their right minds. 110,000 asylum applications in Germany and he wants to take in even more. Dear CSU, send him into retirement at last. #AfD","ans":[{"t":"migrants -> asylum seekers","s":"against","explanation":"The author doesn’t want more asylum seekers in Germany."},{"t":"migration policies -> CSU","s":"against","explanation":"The post critizes the migration policy of CSU (AFD -> favor is also an acceptable answer)."}]}
]
completion_url = "https://app.prolific.com/submissions/complete?cc=CHCBTBHM"
stance_options = ["favor","against","none"]
task_description = """
                    Please determine if the following targets appear in the post, the :red[**question mark**] contains the fine-grained target of each broad target in case you have forgotten. 
                    Once you have selected a target, 
                    please determine its fine-grained target (choose **none** if only the broad target applies) and the stance (choose :red[**none**]
                    if there is no clear stance toward the target, exception: Migration Policies). To cancel your selection, please click :red[**No**]. You can choose :red[**from one to three**] targets."""
lang2id = {"English":"en","German":"de","Greek":"el","Spanish":"es","French":"fr","Hungarian":"hu","Italian":"it","Dutch":"nl","Polish":"pl","Slovak":"sk","Swedish":"sv"}
ttl = 1200

text_css = """
<style>
    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: black;
            z-index: 999;
        }
        .fixed-header {
            background-color: black; /* Black background for dark mode */
            color: white; /* White text for dark mode */
            border-bottom: 1px solid black;
            font-size: 24px;
        }
    }
</style>
"""
def get_colored_css(color:str):
    css = f"""
    <style>
    .highlight-color {
        color: {color};
        font-weight: bold;
    }
        </style>
        """
    return css 
@st.cache_data(ttl=ttl)
def load_anno_data(path:str):
    data = []
    with open(path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data

@st.cache_resource(ttl=ttl)
def init_mongo_clinet() -> MongoClient:
    
    # Create a new client and connect to the server
    client = MongoClient(st.secrets["uri"])
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return client 
    except Exception as e:
        st.warning("connection to database failed, please try again.")
        return e 


def load_results(lang,id,no_cache=False):
    client = init_mongo_clinet()
    if not client:
        return dict() 
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    def no_cache():
        data = col.find_one(query)
        return data if data else dict()
    
    @st.cache_data(ttl=ttl)
    def cache():
        return no_cache()
    return cache() if not no_cache else no_cache()
def match_broad_target(target:str):
    """
    Match the corresponding broad target for the given fine-grained target
    """
    if target in all_targets:
        return target
    for broad_target in all_targets.keys():
        if target in all_targets[broad_target]["fg_targets"]:
            return broad_target
    return "migration policies"

def reformat(data:dict):
    reformated_data = dict()
    regex = r"(.+)_(.+)_(.+)"
    fg_regex = r":red\[(.+)\]"
    for k in data:
        
        if not re.search(regex,k):
            continue 
        st,target,id = k.split("_")
        if st == "s" and data["e" + "_" + target + "_" + id]["value"] == "Yes":
            mtc = re.search(fg_regex,data[k]["label"]).group(1) 
            target = target if mtc == "none" else mtc
            b_target = match_broad_target(target)
           
            if id not in reformated_data:
                reformated_data[id] = []
                reformated_data[id].append((b_target,target,data[k]["value"]))
            else:
                reformated_data[id].append((b_target,target,data[k]["value"]))

    return reformated_data
 
def fetch_from_db():
    """
    fetch the mongo db database to local and reformat the answers 
    """
    root = "anno_results"
    client = init_mongo_clinet()
    if not client:
       
        return None 
    db = client["anno-results"]
    for col_name in db.list_collection_names():
        os.makedirs(root + "/" + col_name,exist_ok=True)
        col = db[col_name]
        for item in col.find():
            path = os.path.join(root,col_name,item["PROLIFIC_PID"]) + ".json"
            rf_data = {"results":reformat(item)}
            with open(path,"w") as f:
                json.dump(rf_data,f) 
    
def load_anno_result(id:str,lang:str,no_cache:bool):
    """
    load the annotation results from the local directory 
    """
    root = "anno_results"
    path = os.path.join(root,lang2id[lang],id) + ".json"
    def no_cache():
        with open(path,"r") as f:
            return json.load(f)
    @st.cache_data(ttl=ttl)
    def cache():
        return no_cache()
    return cache() if not no_cache else no_cache()

def get_text_by_id(id,lang):
    """
    Get the annotation example from the example list by resourceId
    
    """
    path = f"human_data/{lang2id[lang]}.jsonl"
    with open(path, "r") as f:
        for line in f:
            item = json.loads(line)
            if item["resourceId"] == id:
                return item["fullText"]
    return None 

# def get_intercoder_agreement(lang:str,id1,id2):
#     """
#     dir: directory that contains the coding results of the annotation
#     return the agreement between broad targets, fine-grained targets and stance 
#     id1: annotator 1 
#     id2: annotator 2
#     For each tweets annotated by the annotators, calculate the agreement between the annotators. The annotation results for each tweet takes the following format: 
#     {tweet_id:[(broad_target,fine_grained_target,stance)]}
#     We first calculate the agreement between the broad targets, then the fine-grained targets given the same broad target, and finally the stance given the same broad and fine-grained target.
#     """
#     def convert_to_binary(item:list,targets:list): 
#         """
#             convert the selected targets and stance to binary format 
#             item: list of selected targets, fine-grained targets or stance 
#             targets: list of all possible targets, fine-grained targets or stance 
            
#             Example: 
#             item: ["migrants","European Union Institutions"]
#             targets: ["migration policies", "European Union Institutions", "refugee pathways", "reception", "asylum procedures", "migrants"]

#             return: [0,1,0,0,0,1]
#             """
#         # convert targets to binary
#         return  [1 if target in item else 0 for target in targets]
#     def filter_fine_grained_targets(anno1:list,anno2:list):
#         """
#         anno1: annotation results for one tweet by annotator 1. Format: [(broad_target,fine_grained_target,stance)....]
#         anno2: annotation results for one tweet by annotator 2  Format: [(broad_target,fine_grained_target,stance)....] 
#         onle keep the fine-grained target if the broad target is the same for both annotators 
#         """
#         filtered_anno1 = []
#         filtered_anno2 = []
#         for bt1, fg1, stance1 in anno1:
#             for bt2, fg2, stance2 in anno2:
#                 if bt1 == bt2:
#                     filtered_anno1.append((bt1,fg1, stance1))
#                     filtered_anno2.append((bt2,fg2, stance2))
#         return filtered_anno1, filtered_anno2 
#     def filter_stance(anno1:list,anno2:list):
#         """
#         Filter stance by the fine grained targets. (broad targets are already the same)
#         """
#         filtered_anno1 = []
#         filtered_anno2 = []
#         for bt1, fg1, stance1 in anno1:
#             for bt2, fg2, stance2 in anno2:
#                 if fg1 == fg2:
#                     filtered_anno1.append((bt1,fg1, stance1))
#                     filtered_anno2.append((bt2,fg2, stance2))
#         return filtered_anno1, filtered_anno2
    
#     anno_data1 = load_anno_result(id1,lang,False)["results"]
#     anno_data2 = load_anno_result(id2,lang,False)["results"]
#     # get the tweet ids that are annotated by both annotators 
#     all_tweet_ids = set(anno_data1.keys()).intersection(set(anno_data2.keys()))
#     # filter annotation results by the tweet ids that are annotated by both annotators
#     anno_data1 = {k:anno_data1[k] for k in all_tweet_ids}
#     anno_data2 = {k:anno_data2[k] for k in all_tweet_ids}
#     # get the broad targets agreement 
#     broad_targets = list(all_targets.keys()) 
#     broad_targets1 = []
#     broad_targets2 = []

#     # get the fine-grained targets agreement
#     fine_grained_targets1 = []
#     fine_grained_targets2 = []
#     # get stance 
#     stance1 = []
#     stance2 = []
#     stance_options = ["favor","against","none"]
#     for tweet_id in all_tweet_ids:
#         broad_targets1.extend(convert_to_binary([item[0] for item in anno_data1[tweet_id]],broad_targets))
#         broad_targets2.extend(convert_to_binary([item[0] for item in anno_data2[tweet_id]],broad_targets))
#         # filter the fine-grained targets by the broad targets
#         fg1, fg2 = filter_fine_grained_targets(anno_data1[tweet_id],anno_data2[tweet_id]) 
#         fine_grained_targets1.extend(convert_to_binary([item[1] for item in fg1],all_fg_targets))
#         fine_grained_targets2.extend(convert_to_binary([item[1] for item in fg2],all_fg_targets))
#         # filter the stance by the fine-grained targets 
#         st1, st2 = filter_stance(fg1,fg2)
#         stance1.extend(convert_to_binary([item[2] for item in st1],stance_options))
#         stance2.extend(convert_to_binary([item[2] for item in st2],stance_options))


        



#     bt_agreement = cohen_kappa_score(broad_targets1,broad_targets2) 
#     fg_agreement = cohen_kappa_score(fine_grained_targets1,fine_grained_targets2)
#     stance_agreement = cohen_kappa_score(stance1,stance2)

#     return bt_agreement, fg_agreement, stance_agreement


