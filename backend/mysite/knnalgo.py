# k-nearest neighbors for multioutput regression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle
from tools import *

from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import SCORERS

filename = "webapp/algos/knn_model.sav"
model = KNeighborsRegressor(weights='distance', p=1)

# uniqueapls = []

# def parse_vector_string(vectorstr):
#     vectorls = vectorstr.replace("[", "").replace("]", "").replace(" ", "")
#     vectorls = vectorls.split(",")
#     it = iter(vectorls)
#     vectordict = dict(zip(it, it))
#     return vectordict

# def parse_point_string(pointstr):
#     pointls = pointstr.split(",")
#     pointls = [float(i) for i in pointls]
#     return pointls

# def get_superset(vectordictls):
#     # get superset of all APs scanned across floor in alphabetical order
#     uniqueapls.extend(list(set(k for vectordict in vectordictls for k in vectordict.keys())))
#     uniqueapls.sort()

# def clean_vectors(vectordictls):
#     # a vector is a list of the RSSI value of each AP in the superset (and 0 if AP was not detected at a point)
#     result = []
#     for item in vectordictls:
#         inputdict = dict.fromkeys(uniqueapls, 0)
#         inputdict.update(item)
#         inputls = [int(val) for val in inputdict.values()]
#         result.append(inputls)

#     return result

# def filter_aps(testdict):
#     return dict([(key, val) for key, val in testdict.items() if key in uniqueapls])


def train_model(scanmap):
    # #x --> vectors of RSSI values
    # x = []
    # temp_x = []
    # #y --> coordinates of locations
    # y = []

    # for item in scanmap:
    #     vectorstr = item['vector']
    #     temp_x.append(parse_vector_string(vectorstr))
    #     pointstr = item['point']
    #     y.append(parse_point_string(pointstr))

    # get_superset(temp_x)
    # print("Unique APs = ", uniqueapls)
    # x = clean_vectors(temp_x)

    # x --> vectors of RSSI values
    x = []
    # y --> coordinates of locations
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
    # retrieve AP list
    retrieve_aplist()
    testvector = parse_vector_string(testvector)
    testvector = filter_aps(testvector)
    testvector = clean_vectors([testvector])
    result = loaded_model.predict(testvector)
    return result


def evaluate_model(X_data, y_data):
    edist=[]
    # model = RandomForestRegressor(n_estimators = 200, oob_score = True)
    model = KNeighborsRegressor(algorithm='brute', leaf_size=20,
         metric='chebyshev', n_neighbors=4, weights='distance')
    model = optimize(X_data, y_data)
    X = np.array(X_data)
    y = np.array(y_data)
    rkf = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)
    results = cross_val_score(
        model, X, y, cv=rkf, scoring='neg_mean_squared_error')
    print('Metric (MSE): %.3f' % (abs(np.mean(results)))
    for train_idx, test_idx in rkf.split(X):
        X_train, X_test=X[train_idx], X[test_idx]
        y_train, y_test=y[train_idx], y[test_idx]
        model.fit(X_train, y_train)
        preds=model.predict(X_test)
        edist.append(euclidean_distance(y_test, preds))
    print('Euclidean: %.3f' % (np.mean(edist)))


# Hyperparameter tuning
def optimize(x, y):
    model=KNeighborsRegressor()
    params={'n_neighbors': [3, 4, 5, 6],
        'weights': ['uniform', 'distance'],
        'algorithm': ['brute', 'kd_tree', 'ball_tree'],
        'metric': ['manhattan', 'euclidean', 'chebyshev', 'minkowski'],
        'leaf_size': [20, 30, 40]}

    gcv=GridSearchCV(model, param_grid=params, verbose=1)
    gcv.fit(x, y)
    # The best hyper parameters set
    print("Best Hyper Parameters:\n", gcv.best_params_)
    return gcv.best_estimator_
