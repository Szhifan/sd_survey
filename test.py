import streamlit as st 
from pymongo.mongo_client import MongoClient

import pymongo
def init_mongo_clinet() -> MongoClient:
    
    # Create a new client and connect to the server
    client = MongoClient(st.secrets["uri"])
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return client 
    except Exception as e:
        return None 
myclient = init_mongo_clinet()

mydb = myclient["mydatabase"]
mycol = mydb["customers"]

data = [{"name":"姚文元"},{"name":"张春桥"},{"name":"王洪文"},{"name":"江青"}]

query = {"name":"王洪文"}
update = {"$set":{"name":"王洪文","hobby":"茅台"}} 
mycol.update_one(query,update) 