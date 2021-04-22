# mlp for multi-output regression
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.optimizers import Adam
import keras.backend as K
from keras.callbacks import EarlyStopping
from keras.layers import Dense, BatchNormalization, Dropout

from tools import euclidean_distance

# PARAMETERS FOR CNN WITH SAE
training_ratio = 0.9
verbose = 1
seed = 7
sae_activation = 'relu'
sae_bias = False
sae_optimizer = 'adam'
sae_loss = 'mse'
classifier_activation = 'tanh'
classifier_bias = False
classifier_optimizer = 'adam'
classifier_loss = 'mse'
epochs = 20
batch_size = 10
sae_hidden_layers = [int(i) for i in "256,128,64,128,256".split(',')]
dropout = 0.5


def rmse(y_true, y_pred):
	return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))


# simple NN model --> two dense layers
def make_simplenn_model(n_inputs, n_outputs):
	model = Sequential()
	model.add(Dense(20, input_dim=n_inputs,
	          kernel_initializer='he_uniform', activation='relu'))
	model.add(Dense(n_outputs))
	model.compile(loss='mse', metrics='mse', optimizer='adam')
	return model

# NN model --> four dense layers
def make_nn_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(50, input_dim=n_inputs, activation='sigmoid'))
    model.add(BatchNormalization())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(n_outputs, activation='relu'))
    model.compile(loss='mse', metrics='mse', optimizer=Adam(0.001))
    return model


model_dict = {"simpleNN": make_simplenn_model, "NN": make_nn_model}

# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y, model, name):
    results = list()
    edist = list()
    X = np.array(X)
    y = np.array(y)
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # define evaluation procedure
    cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)
    # enumerate folds
    for train_ix, test_ix in cv.split(X):
        # prepare data
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y[train_ix], y[test_ix]
        # fit model
        if name=="simpleNN":
            finalmodel = model
            finalmodel.fit(X_train, y_train, verbose=0, epochs=20)
        elif name=="NN":
            finalmodel = model
            es = EarlyStopping(monitor='val_loss', patience=100, verbose=0, mode='auto', restore_best_weights=True)
            finalmodel.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=25, batch_size=50,  verbose=0, callbacks=[es])
        elif name=="saeCNN":
            # fit encoder
            model.fit(X, X, batch_size=batch_size, epochs=epochs, verbose=verbose)
            # complete and fit model
            finalmodel = make_saecnn_model(n_inputs, n_outputs, model)
            finalmodel.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size=batch_size, epochs=epochs, verbose=verbose)
            
        # calculate euclidean distance
        preds = finalmodel.predict(X_test)
        edist.append(euclidean_distance(y_test, preds))
        # evaluate model on test set
        metrics = finalmodel.evaluate(X_test, y_test, verbose=0)
        results.append(metrics)
    return results, edist
    

def get_evaluation_results(X, y):
    dfls = []
    X = np.array(X)
    y = np.array(y)
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    for m in model_dict:
        # evaluate model
        model = model_dict[m](n_inputs, n_outputs)
        results, edist = evaluate_model(X, y, model, m)
        # summarize performance
        print(m, end=", ")
        print('Metric (MSE): %.3f' % (np.mean(results)), end=", ")
        print('Euclidean distance : %.3f' % (np.mean(edist)))
        dfls.append([m, round(np.mean(results), 3), round(np.mean(edist), 3)])
    return dfls
