# k-nearest neighbors for multioutput regression
from sklearn.neighbors import KNeighborsRegressor
import pickle
from tools import *

model = KNeighborsRegressor(algorithm='ball_tree', leaf_size=20, metric='euclidean', n_neighbors=6, weights='distance')

def train_model(scanmap, filename):
    # x --> vectors of RSSI values
    x = []
    # y --> coordinates of locations
    y = []
    x, y = get_model_inputs(scanmap)

    print("Training vector length: ", len(x[0]))
    model.fit(x, y)
    # save the model to disk
    pickle.dump(model, open(filename, 'wb'))
    return True


def get_trained_model():
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model


def get_prediction(testvector, filename):
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    # retrieve AP list
    retrieve_aplist()
    testvector = parse_vector_string(testvector)
    print("Test vector: ", len(testvector), testvector)
    testvector = filter_aps(testvector)
    print("Test vector: ", len(testvector), testvector)
    testvector = clean_vectors([testvector])
    print("Test vector: ", len(testvector), testvector, len(testvector[0]))
    result = loaded_model.predict(testvector)
    return result
