# k-nearest neighbors for multioutput regression
from sklearn.neighbors import KNeighborsRegressor

model = KNeighborsRegressor(weights='distance', p=1)

def train_model(scanmap):
    #x --> vectors of RSSI values
    x = []
    #y --> coordinates of locations
    y = []
    model.fit(x, y)
    return True

def get_prediction(testvector):
    result = model.predict(testvector)
    return result
