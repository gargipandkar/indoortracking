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
 
# get the model
def get_model(n_inputs, n_outputs):
	model = Sequential()
	model.add(Dense(20, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
	model.add(Dense(n_outputs))
	model.compile(loss=euclidean_distance_loss, metrics=euclidean_distance_loss, optimizer='adam')
	return model

# get the model 2.0
def create_neural_network(input_dimension):
    model = Sequential()
    model.add(Dense(50, input_dim=input_dimension, activation='sigmoid'))
    model.add(BatchNormalization())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(2, activation='relu'))

    model.compile(loss=euclidean_distance_loss, metrics=euclidean_distance_loss, optimizer=Adam(0.001))
    return model

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
		# model = get_model(n_inputs, n_outputs)
		# fit model
		# model.fit(X_train, y_train, verbose=0, epochs=20)

		model = create_neural_network(n_inputs)
		es = EarlyStopping(monitor = 'val_loss', patience = 100, verbose = 0, mode = 'auto', restore_best_weights = True)
		model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=50,  verbose=0, callbacks = [es])
		
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