import pandas as pd
import numpy as np

uniqueapls = []
filename_pred = "models/evaluation.xlsx"
MODEL_NAMES = ["knn", "svr", "extratrees", "randomforest"]
actual_col = "Actual coordinates"

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
    # get superset of all APs scanned across floor in alphabetical order
    uniqueapls.extend(list(set(k for vectordict in vectordictls for k in vectordict.keys())))
    uniqueapls.sort()

def clean_vectors(vectordictls):
    # a vector is a list of the RSSI value of each AP in the superset (and 0 if AP was not detected at a point)
    result = []
    for item in vectordictls:
        inputdict = dict.fromkeys(uniqueapls, 0)
        inputdict.update(item)
        inputls = [int(val) for val in inputdict.values()]
        result.append(inputls)
    
    return result

def remove_aps(testdict):
    # TODO: remove APs that are not fixed
    return dict([(key, val) for key, val in testdict.items() if key in uniqueapls])


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
    print("Unique APs = ", uniqueapls)
    x = clean_vectors(temp_x)

    return x, y

    
def euclidean_distance(actual_ls, pred_ls):
    numpoints = len(pred_ls)
    result = 0
    for i in range(numpoints):
        actual_arr = np.array(actual_ls[i], dtype=np.float32)
        pred_arr = np.array(pred_ls[i], dtype=np.float32)
        result += np.linalg.norm(actual_arr - pred_arr)
        
    result = round(result/numpoints, 3)
    return result
        

def initialize_predfile():
    df = pd.read_excel(filename_pred)
    for m in MODEL_NAMES:
        df[m]=0
    with pd.ExcelWriter(filename_pred) as writer:  
        df.to_excel(writer, sheet_name='values', index=False)

def save_predictions(i, ls):
    df = pd.read_excel(filename_pred)
    # ls should be list of list of floats --> [[1, 2], [1, 1], [3, 2]]
    strls = []
    for m in ls:
        stritem = ",".join([str(coor) for coor in m])
        strls.append(stritem)
    df.loc[i, MODEL_NAMES] = strls
    with pd.ExcelWriter(filename_pred) as writer:  
        df.to_excel(writer, sheet_name='values', index=False)
    

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







        

        