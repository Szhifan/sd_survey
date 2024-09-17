
import re 
import streamlit as st 
import json 
import os 
from pymongo.mongo_client import MongoClient
all_targets = {
"migration policies":{"fg_targets":["policies of a political entity (party, country or politician) or 'concret policy name' (e.g. Brexit)","EU-Turkey refugee return agreement","Dublin Regulation","Refugee Quotas"]},
"European Union Institutions":{"fg_targets":["none","European Parliament","European Commission", "European Council","FRONTEX","ECHO"]},
"refugee pathways":{"fg_targets":["none","boat sinking","Mediterranean crossing","smuggling"]},
"reception":{"fg_targets":["none","refugee camps"]},
"asylum procedures":{"fg_targets":["none","protection", "compensation", "legal rights"]},
"migrants":{"fg_targets":["none","illegal migrants","refugees","asylum seekers","economic migrants",]}
} 
examples = [
{"text":"Poland, Czech Republic, and Hungary, I advise you to :red[resist the pressure of the EU] to import :red[migrants]. If you need even more motivation, just look at Germany and Sweden.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The author of the post supports the hard-line asylum policies of Poland, Czechia and Hungary while hinting at the severe consequences of taking up migrants like Germany and Sweden. Although the post only mentions migrants, given the background knowledge of the 2014 refugee crisis the migrants here are the refugees from the Middle East. So the fine-grained target should be refugee."},{"t":"European Union Institutions -> none","s":"against","explanation":"The phrase 'pressure of the EU' indicates, given enough background knowledge, that the EU pressured its member states to accommodate refugees during the refugee. In this case,  'EU' is not merely a place name but a political institution that enacts laws and makes political decisions. Since no specific EU institution name such as EU parliament is mentioned, a fine-grained target is not applicable in this case. Also, the author criticises EU for its policies."}]},
{"text":"To the delusional leftists, Obama, Merkel, the Canadian Prime Minister, Pope Francis, United Nations, and others they say nothing goes wrong even though there are ongoing terrorism problems due to the :red[refugees and illegal aliens] in the EU and other places.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The post directly mentions “refugee” and concerns the mass influx of non-EU migrants. Note: “EU institutions” is not a target here because the author merely indicates that the refugees are coming to the “EU”, but the EU here is a place where the issue takes place rather than a political agency."}]},
{"text":":green[Salvini refuses to bend, I love it]. Italy - Salvini :red[Refuses To Let 177 Migrants] :orange[Off Ship] Till EU Agrees To Take Them (Video) news","ans":[{"t":"migrants -> refugees","s":"against","explanation":"Salvini is a right-wing Italian politician holding anti-migrant opinions. The post supports his hard-line policies against refugees thus the post is against the refugees."},{"t":"refugee pathways -> Mediterranean crossing","s":"none","explanation":"The mentions refugees coming to the EU by boat through the Mediterranean Sea, while no further stance is expressed."},{"t":"migration policies -> Salvini","s":"favor","explanation":"The post stongly support the migration policy of Salvini."}]},
{"text":"The funny thing about :red[Brexit is that even the racists will be disappointed by it]. The UK is not going to expel 2 million :green[EU workers otherwise economy collapses]. & future immigration more likely to come from Africa/Asia as Europeans won’t want to come without guaranteed rights.","ans":[{"t":"migrants -> economic migrants","s":"favor","explanation":"The post primarily mentions migrants and specifically concerns about the economic consequences of EU migrants leaving UK and acknowledges their contributions to the UK economy. Thus, the post talks about economic migrants from EU/Africa/Asia who come to the UK for career perspectives."},{"t":"migration policies -> UK","s":"against","explanation":"The post critizes the economic consequences of Brexit."}]},
{"text":"(translated from German)RT @warum_nur74 @Beatrix_vStorch The EU (SPD HrTönnes) wants to do it that way too. :green[Suspend Dublin] and then if a :red[refugee] in Libya says that his relative is in Germany, :orange[he comes straight to Germany. He doesn't need papers]. The word is enough. Sometimes I wish for other times.","ans":[{"t":"migrants -> refugees","s":"against","explanation":"The author wants a more tightened control of refugees, indicating a against stance toward refugees."},{"t":"migration policies -> Dublin Regulation","s":"favor","explanation":"The author of the post supports the Dublin Regulation that it regulates which refugee should be allocated to which EU country. Otherwise, the refugees will pick whatever country they like (especially wealthy EU country like Germany). (Migration Policies -> SPD -> against is an alternative answer.)"},{"t":"asylum procedures -> none","s":"none","explanation":"The author talks about the way and procedures a refugee is allocated to the receiving country (either through the Dublin agreement or depending on their relatives in Germany). But there is no clear stance towards this topic."}]},
{"text":"(translated from German)RT @Beatrix_vStorch :red[Migrant distribution] minister Seehofer is failing because of the EU states. Unlike the minister, they are still in their right minds. 110,000 asylum applications in Germany and he wants to take in even more. :red[Dear CSU, send him into retirement at last]. #AfD","ans":[{"t":"migrants -> asylum seekers","s":"against","explanation":"The author doesn’t want more asylum seekers in Germany."},{"t":"migration policies -> CSU","s":"against","explanation":"The post critizes the migration policy of CSU (AFD -> favor is also an acceptable answer)."}]}
]
completion_url = "https://app.prolific.com/submissions/complete?cc=CHCBTBHM"
stance_options = ["favor","against","none"]
task_description = "Please determine if the following targets appear in the post, the :red[**question mark**] contains the fine-grained target of each broad target in case you have forgotten. Once you have selected a target, please determine its fine-grained target (choose :red[**none**] if no fine-grained target applies) and the stance (choose :red[**none**] if there is no clear stance toward the target). To cancel your selection, please click :red[**No**] .You can choose up to :red[**from one to three**] targets."
lang2id = {"English":"en","German":"de","Greek":"el","Spanish":"es","French":"fr","Hungarian":"hu","Italian":"it","Dutch":"nl","Polish":"pl","Slovak":"sk","Swedish":"sv"}
ttl = 1200


@st.cache_data(ttl=ttl)
def get_anno_data(path:str):
    with open(path,"r") as f:
        return json.load(f)

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
def load_results_no_cache(lang,id):
    client = init_mongo_clinet()
    if not client:
       
        return dict()
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    user_data = col.find_one(query)
    return user_data if user_data else dict()

def load_results(lang,id,no_cache=False):
    client = init_mongo_clinet()
    if not client:
        return dict() 
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    def no_cache():
        return col.find_one(query)
    
    @st.cache_data(ttl=ttl)
    def cache():
        return no_cache()
    return cache() if not no_cache else no_cache()


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
           
            if id not in reformated_data:
                reformated_data[id] = []
                reformated_data[id].append((target,data[k]["value"]))
            else:
                reformated_data[id].append((target,data[k]["value"]))

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
    path = f"data/{lang2id[lang]}.json"
    with open(path,"r") as f:
        data = json.load(f)
        for item in data:
            if item["resourceId"] == id:
                return item["fullText"]
    return None 
    

if __name__ == "__main__":

    fetch_from_db()