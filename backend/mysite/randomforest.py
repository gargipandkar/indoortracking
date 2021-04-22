from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle
from tools import *

filename = "webapp/algos/randomforest_model.sav"
# Optimized model based on GridSearchCV
model = RandomForestRegressor( criterion='mae', max_depth=20, 
                            max_features= 'auto', n_estimators= 150)

def train_model(scanmap):
    #x --> vectors of RSSI values
    x = []
    #y --> coordinates of locations
    y = []
    x, y = tools.get_model_inputs(scanmap)
    
    #print("training") #debug
    #model = optimize(x,y)
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

# Hyperparameter tuning
def optimize(x,y):
    print("Optimizing")
    model = RandomForestRegressor()
    params = {'criterion':['mae','mse'],
        'max_depth': [10, 20, 30, 40],
        'max_features': ['auto', 'sqrt'],
        'n_estimators': [150,200,250],}

    gcv = GridSearchCV(model, param_grid=params)
    gcv.fit(x,y)
    print("done optimizing")
    #The best hyper parameters set
    print("Best Hyper Parameters:\n",gcv.best_params_)
    return gcv.best_estimator_