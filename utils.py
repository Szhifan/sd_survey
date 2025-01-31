
import re 
import streamlit as st 
import json 
import os 
from pymongo.mongo_client import MongoClient 
from interface_utils import ALL_TARGETS,LANG2ID,TTL


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
@st.cache_data(ttl=TTL)
def load_anno_data_partition(path:str,n=None,partition=None):
    with open(path, "r") as f:
        data = json.load(f)
        if not n and not partition:
            return data
        data = data[:n]
        if partition == "1":
            return data[:n//2]
        elif partition == "0":
            return data
        else:
            return data[n//2:]
@st.cache_data(ttl=TTL)
def load_anno_data(path:str,n=None,include_id:list=None):
    with open(path, "r") as f:
        data = json.load(f)
        if include_id:
            data = [item for item in data if item["resourceId"] in include_id]
        if not n:
            return data
        return data[:n]
@st.cache_resource(ttl=TTL)
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
def load_results(lang,id,no_cache=False,db_name="anno-results",study_id=None):
    client = init_mongo_clinet()
    if not client:
        return dict() 
    db = client[db_name]
    col = db[LANG2ID.get(lang,lang)]
    query = {"PROLIFIC_PID":id}
    if study_id:
        query["study_id"] = study_id
    def no_cache():
        data = col.find_one(query)
        return data if data else dict()
    
    @st.cache_data(ttl=TTL)
    def cache():
        return no_cache()
    return cache() if not no_cache else no_cache()
def match_broad_target(target:str):
    """
    Match the corresponding broad target for the given fine-grained target
    """
    if target in ALL_TARGETS:
        return target
    for broad_target in ALL_TARGETS.keys():
        if target in ALL_TARGETS[broad_target]["fg_targets"]:
            return broad_target
    return "migration policies"

def reformat_target(data:dict):
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
                reformated_data[id].append({
                    "target":b_target,
                    "fg_target":target,
                    "stance":data[k]["value"]
                })
            else:
                reformated_data[id].append({
                    "target":b_target,
                    "fg_target":target,
                    "stance":data[k]["value"]
                }
                )


    reformated_data["time_spent"] = data.get("time_spent")
   
    return reformated_data

def reformat_stance(data:dict):
    """
    restructuring the data
    structure: 
    {
        id1: {target: {target_relevance: "relevant", "fg_target_relevance": "relevant", "stance": "favor"}},
        id2: {target: {target_relevance: "relevant", "fg_target_relevance": "relevant", "stance": "favor"}},
        ... 
    }
    """
    results = {}
    for key in data:
        split = key.split("_")
        if len(split) != 3:
            continue
        task, target, id = split
        if id not in results:
            results[id] = {}
        if target not in results[id]:
            results[id][target] = {}
        if task == "r":
            results[id][target]["target_relevance"] = data[key]["value"]
        elif task == "rft":
            results[id][target]["fg_target_relevance"] = data[key]["value"]
            if not results[id][target]["fg_target_relevance"]:
                results[id][target]["fg_target_relevance"] = results[id][target]["target_relevance"]
        elif task == "st":
            results[id][target]["stance"] = data[key]["value"]
    # fetch other fileds
    results["completed"] = len(results)
    completed = results["completed"]
    prolific_id = data.get("PROLIFIC_PID")
    print(f"id: {prolific_id} has completed {completed} tasks")
    results["test_passed"] = data.get("test_passed")
    results["partition"] = data.get("partition")
    time_spent = data.get("what is the total time you spent on this task? (in minutes)")
    if time_spent:
        results["time_spent"] = time_spent["value"]
    return results

 
def fetch_from_db(lang:str,id:str,db_name:str="anno-results"):
    """
    fetch the mongo db database to local and reformat the answers 
    """
    root = db_name
    reformat = reformat_target if db_name == "anno-results" else reformat_stance
    client = init_mongo_clinet()
    if not client:
        return None 

    db = client[db_name]

    col = db[lang]
    rf_data = {}
    path_save = os.path.join(root,lang,id) + ".json"
    os.makedirs(os.path.dirname(path_save),exist_ok=True)
    for item in col.find():
        if item["PROLIFIC_PID"] == id:
            rf_data.update(reformat(item))
    with open(path_save,"w") as f:
        json.dump(rf_data,f,indent=4) 

    
def load_anno_result(id:str,lang_id:str,no_cache:bool,path:str = "anno_results"):
    """
    load the annotation results from the local directory 
    """

    path = os.path.join(path, lang_id, id) + ".json"
    if not os.path.exists(path):
        return {}

    def no_cache():
        with open(path, "r") as f:
            return json.load(f)

    @st.cache_data(ttl=TTL)
    def cache():
        return no_cache()

    return cache() if not no_cache else no_cache()

def get_text_by_id(id,lang_id):
    """
    Get the annotation example from the example list by resourceId
    
    """
    
    if lang_id == "en" or lang_id == "de":
        path = f"human_data/{lang_id}.json" 
    else: 
        path = f"data_translated/{lang_id}.json"
    with open(path,"r") as f:
        data = json.load(f)
    for item in data:
        if item["resourceId"] == id:
            return item["fullText"]
    return None 

if __name__ == "__main__":
    fetch_from_db("pl2en","665dd746f5ea0c66ebd85edb","anno-xculture")