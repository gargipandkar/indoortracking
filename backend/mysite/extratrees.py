from sklearn.tree import ExtraTreeRegressor

model = ExtraTreeRegressor(splitter = 'best')

def parse_vector_string(vectorstr):
    vectorls = vectorstr.replace("[", "").replace("]", "").replace(" ", "")
    vectorls = vectorls.split(",")
    it = iter(vectorls)
    vectordict = dict(zip(it, it))
    return vectordict

def parse_point_string(pointstr):
    pointls = pointstr.split(",")
    return pointls

def clean_vectors(vectordictls):
    uniqueapls = list(set(k for vectordict in vectordictls for k in vectordict.keys()))
    uniqueapls.sort()

    result = []
    for item in vectordictls:
        inputdict = dict.fromkeys(uniqueapls, 0)
        inputdict.update(item)
        inputls = [int(val) for val in inputdict.values()]
        result.append(inputls)
    
    return result


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

    x = clean_vectors(temp_x)
    # return x

    model.fit(x, y)
    return True

def get_prediction(testvector):
    testvector = parse_vector_string(testvector)
    testvector = clean_vectors(list(testvector))[0]
    result = model.predict(testvector)
    return result