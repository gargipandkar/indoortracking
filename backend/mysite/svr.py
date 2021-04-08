from sklearn.svm import SVR
import pickle
from tools import *

filename = "webapp/algos/svr_model.sav"

model = SVR('poly')

# def train_model(scanmap):
#     #x --> vectors of RSSI values
#     x = []
#     temp_x = []
#     #y --> coordinates of locations
#     y = []
  
#     for item in scanmap:
#         vectorstr = item['vector']
#         temp_x.append(parse_vector_string(vectorstr))
#         pointstr = item['point']
#         y.append(parse_point_string(pointstr))

#     x = clean_vectors(temp_x)
#     # return x

#     model.fit(x, y)
#     return True

# def get_prediction(testvector):
#     testvector = parse_vector_string(testvector)
#     testvector = clean_vectors(list(testvector))[0]
#     result = model.predict(testvector)
#     return result

def train_model(scanmap):
    #x --> vectors of RSSI values
    x = []
    #y --> coordinates of locations
    y = []
    x, y = get_model_inputs(scanmap)

    model.fit(x, y)
    # save the model to disk
    pickle.dump(model, open(filename, 'wb'))
   
    return True
def get_trained_model():
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model

def get_prediction(testvector):
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    testvector = parse_vector_string(testvector)
    testvector = filter_aps(testvector)
    testvector = clean_vectors([testvector])
    result = loaded_model.predict(testvector)
    return result
