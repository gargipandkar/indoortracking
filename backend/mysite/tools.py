import pandas as pd
import numpy as np
from webapp.models import Floorplan

uniqueapls = []
MODEL_NAMES = ["knn", "extratrees", "randomforest"]
CURRENT_PLAN = ""

def set_current_plan(plan):
    global CURRENT_PLAN
    global filename_pred
    CURRENT_PLAN = plan

def parse_vector_string(vectorstr):
    vectorls = vectorstr.replace("[", "").replace("]", "").replace(" ", "")
    vectorls = vectorls.split(",")
    it = iter(vectorls)
    vectordict = dict(zip(it, it))
    return vectordict

def parse_point_string(pointstr):
    pointls = pointstr.split(",")
    pointls = [float(i) for i in pointls]
    return pointls

def get_superset(vectordictls):
    global uniqueapls
    global CURRENT_PLAN
    # get superset of all APs scanned across floor in alphabetical order
    uniqueapls.clear()
    uniqueapls.extend(list(set(k for vectordict in vectordictls for k in vectordict.keys())))
    uniqueapls.sort()
    # save_aplist(CURRENT_PLAN, uniqueapls)

def clean_vectors(vectordictls):
    # a vector is a list of the RSSI value of each AP in the superset (and 0 if AP was not detected at a point)
    result = []
    for item in vectordictls:
        print("Unique AP length: ",len(uniqueapls))
        inputdict = dict.fromkeys(uniqueapls, 0)
        inputdict.update(item)
        inputls = [int(val) for val in inputdict.values()]
        result.append(inputls)
    
    return result

def filter_aps(testdict):
    global uniqueapls
    # return dict([(key, val) for key, val in testdict.items() if key in uniqueapls])
    # only consider fixed APs --> any of the SUTD networks or eduroam
    return dict([(key, val) for key, val in testdict.items() if key in uniqueapls and ("SUTD_Wifi" in key or "SUTD_Guest" in key or "eduroam" in key)])

def save_aplist(currentplan, ls):
    print(currentplan)
    planobj = Floorplan.objects.get(title=currentplan)
    planobj.aplist = ls
    planobj.save()

def save_cleaned_aplist(currentplan):
    planobj = Floorplan.objects.get(title=currentplan)
    ls = planobj.aplist
    ls = ls.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    ls = ls.split(",")
    cleanls = [item for item in ls if "SUTD_Wifi" in item or "SUTD_Guest" in item or "eduroam" in item]
    print("Cleaned AP list: ", cleanls)
    planobj.aplist = cleanls
    planobj.save()

def retrieve_aplist():
    global uniqueapls
    global CURRENT_PLAN
    planobj = Floorplan.objects.get(title=CURRENT_PLAN)
    uniqueapls.clear()
    uniqueapls = planobj.aplist
    uniqueapls = uniqueapls.replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
    uniqueapls = uniqueapls.split(",")
    print("Retrieved: ", len(uniqueapls))

def get_model_inputs(scanmap):
    #x --> vectors of RSSI values
    x = []
    temp_x = []
    #y --> coordinates of locations
    y = []
  
    for item in scanmap:
        vectorstr = item['vector']
        temp_x.append(parse_vector_string(vectorstr))
        pointstr = item['point']
        y.append(parse_point_string(pointstr))

    get_superset(temp_x)
    
    x = clean_vectors(temp_x)
    print("Training vector: ", len(x[0]))

    return x, y

def get_uniqueapls():
    global uniqueapls
    return uniqueapls

def euclidean_distance(actual_ls, pred_ls):
    numpoints = len(pred_ls)
    result = 0
    for i in range(numpoints):
        actual_arr = np.array(actual_ls[i], dtype=np.float32)
        pred_arr = np.array(pred_ls[i], dtype=np.float32)
        result += np.linalg.norm(actual_arr - pred_arr)
        
    result = round(result/numpoints, 3)
    return result
        
    

def evaluate_models():
    df = pd.read_excel(filename_pred)
    actual_ls = [item.split(",") for item in df[actual_col].to_list()]

    metric_dict = {}
    for col in df.columns:
        if col != actual_col:
            ls = df[col].to_list()
            ls = [item.split(",") for item in ls]
            avg_dist = euclidean_distance(actual_ls, ls)
            metric_dict[col] = [avg_dist]
            
    metricdf=pd.DataFrame.from_dict(metric_dict)
    with pd.ExcelWriter(filename_pred) as writer:  
        df.to_excel(writer, sheet_name='values', index=False)
        metricdf.to_excel(writer, sheet_name='metrics', index=False)


def export_data(x, y):
    df = pd.read_excel(filename_pred)
    actual_ls = [item.split(",") for item in df[actual_col].to_list()]

    metric_dict = {}
    for col in df.columns:
        if col != actual_col:
            ls = df[col].to_list()
            ls = [item.split(",") for item in ls]
            avg_dist = euclidean_distance(actual_ls, ls)
            metric_dict[col] = [avg_dist]
            
    metricdf=pd.DataFrame.from_dict(metric_dict)
    with pd.ExcelWriter(filename_pred) as writer:  
        df.to_excel(writer, sheet_name='values', index=False)




        

        