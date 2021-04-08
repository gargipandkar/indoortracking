from sklearn.tree import ExtraTreeRegressor
import pickle
from tools import *

filename = "webapp/algos/extratrees_model.sav"

model = ExtraTreeRegressor(splitter = 'best')

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
