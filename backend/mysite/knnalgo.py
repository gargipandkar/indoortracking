# k-nearest neighbors for multioutput regression
from sklearn.neighbors import KNeighborsRegressor

model = KNeighborsRegressor(weights='distance', p=1)
filename = 'knn_model.sav'
uniqueapls = []

def parse_vector_string(vectorstr):
    vectorls = vectorstr.replace("[", "").replace("]", "").replace(" ", "")
    vectorls = vectorls.split(",")
    it = iter(vectorls)
    vectordict = dict(zip(it, it))
    return vectordict

def parse_point_string(pointstr):
    pointls = pointstr.split(",")
    return pointls

def get_superset(vectordictls):
    # get superset of all APs scanned across floor in alphabetical order
    uniqueapls = list(set(k for vectordict in vectordictls for k in vectordict.keys()))
    uniqueapls.sort()

def clean_vectors(vectordictls):
    # a vector is a list of the RSSI value of each AP in the superset (and 0 if AP was not detected at a point)
    result = []
    for item in vectordictls:
        inputdict = dict.fromkeys(uniqueapls, 0)
        inputdict.update(item)
        inputls = [int(val) for val in inputdict.values()]
        result.append(inputls)
    
    return result

def remove_aps(testdict):
    return dict([(key, val) for key, val in testdict.items() if key in uniqueapls])

def train_model(scanmap):
    #x --> vectors of RSSI values
    x = []
    temp_x = []
    #y --> coordinates of locations
    y = []
  
    for item in scanmap:
        vectorstr = item['vector']
        temp_x.append(parse_vector_string(vectorstr))
        pointstr = item['point']
        y.append(parse_point_string(pointstr))

    get_superset(temp_x)
    x = clean_vectors(temp_x)

    model.fit(x, y)
    # save the model to disk
    pickle.dump(model, open(filename, 'wb'))
   
    return True

def get_prediction(testvector):
    # load the model from disk
    # loaded_model = pickle.load(open(filename, 'rb'))
    testvector = parse_vector_string(testvector)
    testvector = remove_aps(testvector)
    testvector = clean_vectors([testvector])
    result = model.predict(testvector)
    return result
