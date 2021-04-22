# mlp for multi-output regression
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout
from keras.optimizers import Adam
import keras.backend as K
from keras.callbacks import EarlyStopping

from tools import euclidean_distance

# set paramter values
# ------------------------------------------------------------------------
# general
training_ratio = 0.9           
output_dim = 2                 
verbose = 0                     
seed = 7    
epochs = 20
batch_size = 10                    
# ------------------------------------------------------------------------
# stacked auto encoder (sae)
sae_activation = 'relu'
sae_bias = False
sae_optimizer = 'adam'
sae_loss = 'mse'
sae_hidden_layers = [int(i) for i in "256,128,64,128,256".split(',')]
# ------------------------------------------------------------------------
# classifier
classifier_activation = 'tanh'
classifier_bias = False
classifier_optimizer = 'adam'
classifier_loss = 'mse'
dropout = 0.5


def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))

def get_sae_encoder(input_dim):
    # create a model based on stacked autoencoder (SAE)
    model = Sequential()
    model.add(Dense(sae_hidden_layers[0], input_dim=input_dim,
                    activation=sae_activation, use_bias=sae_bias))
    for units in sae_hidden_layers[1:]:
        model.add(Dense(units, activation=sae_activation, use_bias=sae_bias))
    model.add(Dense(input_dim, activation=sae_activation, use_bias=sae_bias))
    model.compile(optimizer=sae_optimizer, loss=sae_loss)
    return model


def get_sae_model(n_inputs, model):
    # remove the decoder part
    num_to_remove = (len(sae_hidden_layers) + 1) // 2
    for i in range(num_to_remove):
        model.pop()

    # set all layers (i.e., SAE encoder) to non-trainable (weights will not be updated)
    # for layer in model.layers[:]:
    #     layer.trainable = False
    
    # build complete model with the trained SAE encoder
    # model.add(Dropout(dropout))
    model.add(Dense(output_dim))
    model.compile(optimizer=classifier_optimizer, loss=classifier_loss, metrics='mse')
    return model

# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y):
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
        # encoder
        encodermodel = get_sae_encoder(n_inputs)
        encodermodel.fit(X, X, batch_size=batch_size,
                         epochs=epochs, verbose=verbose)
        # complete model
        finalmodel = get_sae_model(n_inputs, encodermodel)
        # fit model
        finalmodel.fit(X_train, y_train, validation_data=(X_test, y_test),
                  batch_size=batch_size, epochs=epochs, verbose=verbose)

        # calculate euclidean distance
        preds = finalmodel.predict(X_test)
        edist.append(euclidean_distance(y_test, preds))
        # evaluate model on test set
        metrics = finalmodel.evaluate(X_test, y_test, verbose=0)
        results.append(metrics)
    return results, edist
    

def get_evaluation_results(X, y):
    results, edist = evaluate_model(X, y)
    # summarize performance
    m = "saeCNN"
    print(m, end=", ")
    print('Metric (MSE): %.3f' % (np.mean(results)), end=", ")
    print('Euclidean distance : %.3f' % (np.mean(edist)))
    return [[m, round(np.mean(results), 3), round(np.mean(edist), 3)]]



