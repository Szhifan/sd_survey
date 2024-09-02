import pandas as pd 
import json 
import os 
for p in os.listdir("annotated_data"):
    fp = os.path.join("annotated_data",p)
 
    df = pd.read_csv(fp)
    js_l = df.to_json(orient="records")
    obj = json.loads(js_l)[:4]

    
    l,_ = p.split(".")
    with open("data/" + l + ".json","w") as f:
        json.dump(obj,f)