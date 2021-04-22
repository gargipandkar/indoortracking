from sklearn.tree import ExtraTreeRegressor
from sklearn.model_selection import GridSearchCV
import pickle
import tools

filename = "webapp/algos/extratrees_model.sav"

# OPtimized model after GridSearchCV
model = ExtraTreeRegressor(criterion='mse', max_depth= 10, max_features='auto', 
        min_samples_leaf= 1, min_samples_split= 2, splitter='random')

def train_model(scanmap):
    #x --> vectors of RSSI values
    x = []
    #y --> coordinates of locations
    y = []
    x, y = get_model_inputs(scanmap)

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
    model = ExtraTreeRegressor()
    params = {'criterion':['mae','mse','friedman_mse'],
        'max_depth': [10, 20, 30, None],
        'max_features': ['auto', 'sqrt','log2'],
        'min_samples_leaf': [1, 2, 4],
        'min_samples_split': [2, 5, 10],
        'splitter': ['random', 'best']}

    #print("optimizing") #debug
    gcv = GridSearchCV(model, param_grid=params)
    gcv.fit(x,y)
    #The best hyper parameters set
    print("Best Hyper Parameters:\n",gcv.best_params_)
    return gcv.best_estimator_