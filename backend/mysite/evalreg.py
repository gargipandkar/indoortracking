# k-nearest neighbors for multioutput regression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.model_selection import GridSearchCV
import pickle
from tools import *

from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import SCORERS

def get_tunedknn_model(X_data, y_data):
    # for large space, best params --> {'algorithm': 'ball_tree', 'leaf_size': 20, 'metric': 'euclidean', 'n_neighbors': 6, 'weights': 'distance'}
    # for small space, best params --> {'algorithm': 'kd_tree', 'leaf_size': 40, 'metric': 'manhattan', 'n_neighbors': 3, 'weights': 'distance'}
    # model = KNeighborsRegressor(algorithm='brute', leaf_size=20, metric='chebyshev', n_neighbors=4, weights='distance')
    model = optimize_knn(X_data, y_data)
    return model

def get_tunedrf_model(X_data, y_data):
    model = RandomForestRegressor( criterion='mae', max_depth=20, max_features= 'auto', n_estimators= 150)
    return model

def get_tunedet_model(X_data, y_data):
    model = ExtraTreeRegressor(criterion='mse', max_depth= 10, max_features='auto', min_samples_leaf= 1, min_samples_split= 2, splitter='random')
    # model = optimize_et(X_data, y_data)
    return model
    
def evaluate_model(X_data, y_data, model):
    edist=[]
    X = np.array(X_data)
    y = np.array(y_data)
    # evaluate models
    rkf = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)
    results = cross_val_score(model, X, y, cv=rkf, scoring='neg_mean_squared_error')
    # calculate euclidean distance
    for train_idx, test_idx in rkf.split(X):
        X_train, X_test=X[train_idx], X[test_idx]
        y_train, y_test=y[train_idx], y[test_idx]
        model.fit(X_train, y_train)
        preds=model.predict(X_test)
        edist.append(euclidean_distance(y_test, preds))
    return results, edist


# model_dict={"knn": get_tunedknn_model, "randomforest": get_tunedrf_model, "extratrees": get_tunedet_model}
model_dict={"knn": get_tunedknn_model}

def get_evaluation_results(X, y):
    dfls = []
    X = np.array(X)
    y = np.array(y)
    for m in model_dict:
        # evaluate model
        model = model_dict[m](X, y)
        results, edist = evaluate_model(X, y, model)
        # summarize performance
        print(m, end=", ")
        print('Metric (MSE): %.3f' % (np.mean(results)), end=", ")
        print('Euclidean distance : %.3f' % (np.mean(edist)))
        dfls.append([m, round(abs(np.mean(results)), 3), round(np.mean(edist), 3)])
    return dfls

    
# Hyperparameter tuning for KNN
def optimize_knn(x, y):
    model = KNeighborsRegressor()
    params={'n_neighbors': [3, 4, 5, 6],
        'weights': ['uniform', 'distance'],
        'algorithm': ['brute', 'kd_tree', 'ball_tree'],
        'metric': ['manhattan', 'euclidean', 'chebyshev', 'minkowski'],
        'leaf_size': [20, 30, 40]}

    gcv=GridSearchCV(model, param_grid=params, verbose=1)
    gcv.fit(x, y)
    # The best hyper parameters set
    print("Best Hyper Parameters for KNN:\n", gcv.best_params_)
    return gcv.best_estimator_

# Hyperparameter tuning for Extra Trees
def optimize_et(x,y, ):
    model = ExtraTreeRegressor()
    params = {'criterion':['mae','mse','friedman_mse'],
        'max_depth': [10, 20, 30, None],
        'max_features': ['auto', 'sqrt','log2'],
        'min_samples_leaf': [1, 2, 4],
        'min_samples_split': [2, 5, 10],
        'splitter': ['random', 'best']}
    
    gcv = GridSearchCV(model, param_grid=params)
    gcv.fit(x,y)
    #The best hyper parameters set
    print("Best Hyper Parameters for Extra Trees:\n",gcv.best_params_)
    return gcv.best_estimator_
