# mlp for multi-output regression
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization
from keras.optimizers import Adam
import keras.backend as K
from keras.callbacks import EarlyStopping

def euclidean_distance_loss(y_true, y_pred):
	return K.sqrt(K.sum(K.square(y_pred - y_true), axis=-1))
 
def rmse(y_true, y_pred):
	return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))
 
# make a dataset
def make_dataset():
	X, y = make_regression(n_samples=1000, n_features=10, n_informative=5, n_targets=3, random_state=2)
	return X, y

# get the dataset
def get_dataset():
	pass
 

def get_sae_model(n_inputs):

	# create a model based on stacked autoencoder (SAE)
    model = Sequential()
    model.add(Dense(sae_hidden_layers[0], input_dim=input_dim, activation=sae_activation, use_bias=sae_bias))
    for units in sae_hidden_layers[1:]:
        model.add(Dense(units, activation=sae_activation, use_bias=sae_bias))  
	model.add(Dense(input_dim, activation=sae_activation, use_bias=sae_bias))
    model.compile(optimizer=sae_optimizer, loss=sae_loss)

    # train the model
    model.fit(x_train, x_train, batch_size=batch_size, epochs=epochs, verbose=verbose)

    # remove the decoder part
    num_to_remove = (len(sae_hidden_layers) + 1) // 2
    for i in range(num_to_remove):
        model.pop()

    # set all layers (i.e., SAE encoder) to non-trainable (weights will not be updated)
    # for layer in model.layers[:]:
    #     layer.trainable = False

    #build and evaluate a complete model with the trained SAE encoder and a new classifier
    model.add(Dropout(dropout))
    for units in classifier_hidden_layers:
        model.add(Dense(units, activation=classifier_activation, use_bias=classifier_bias))
        model.add(Dropout(dropout))
    model.add(Dense(output_dim, activation='softmax', use_bias=classifier_bias))
    model.compile(optimizer=classifier_optimizer, loss=classifier_loss, metrics=['accuracy'])
 
# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y):
	results = list()
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
		# define model
		model = get_sae_model(n_inputs)
		# fit model
		
		# evaluate model on test set
		metrics = model.evaluate(X_test, y_test, verbose=0)
		# store result
		print(metrics)
		results.append(metrics)
	return results
 
def train_model(X_data, y_data):
	# load dataset
	X, y = X_data, y_data
	print(X, y)
	# evaluate model
	results = evaluate_model(X, y)
	# summarize performance
	print('Euclidean distance: %.3f (%.3f)' % (np.mean(results), np.std(results)))