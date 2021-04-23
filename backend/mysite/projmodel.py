# mlp for multi-output regression
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Dropout
from keras.optimizers import Adam
import keras.backend as K
from keras.callbacks import EarlyStopping

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

# k-nearest neighbors for multioutput regression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV

import pickle
from tools import *

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
    # build complete model with the trained SAE encoder
    # model.add(Dropout(dropout))
    model.add(Dense(output_dim))
    model.compile(optimizer=classifier_optimizer, loss=classifier_loss, metrics='mse')
    return model


def bestReg():
    model = KNeighborsRegressor(algorithm='ball_tree', leaf_size=20, metric='euclidean', n_neighbors=6, weights='distance')
    return model

def train_model(scanmap, filename):
    # x --> vectors of RSSI values
    x = []
    # y --> coordinates of locations
    y = []
    x, y = get_model_inputs(scanmap)

    model.fit(x, y)
    # save the model to disk
    pickle.dump(model, open(filename, 'wb'))
    return True

def get_prediction(testvector, filename):
    # load the model from disk
    loaded_model = pickle.load(open(filename, 'rb'))
    # retrieve AP list
    retrieve_aplist()
    testvector = parse_vector_string(testvector)
    testvector = filter_aps(testvector)
    testvector = clean_vectors([testvector])
    result = loaded_model.predict(testvector)
    return result