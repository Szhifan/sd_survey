
import re 
import streamlit as st 
import json 
import os 
from pymongo.mongo_client import MongoClient
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
@st.cache_data(ttl=ttl,show_spinner="loading your previously stored results")
def load_results_cache(lang,id):
 
    client = init_mongo_clinet()
    if not client:
        return dict() 
    db = client["anno-results"]
    col = db[lang2id[lang]]
    query = {"PROLIFIC_PID":id}
    user_data = col.find_one(query)
    return user_data if user_data else dict()

def load_results(lang,id,use_cache=False):
    return load_results_no_cache(lang,id) if use_cache else load_results_cache(lang,id)


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
            rf_data = reformat(item)
            with open(path,"w") as f:
                json.dump(rf_data,f)
if __name__ == "__main__":

    fetch_from_db()