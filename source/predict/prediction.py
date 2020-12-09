"""Prediction engine
"""
import json
import pickle

import numpy as np
from sklearn.linear_model import LinearRegression
#import joblib

__location = None
__data_columns = None
__model = None

def load_files():

    global __location
    global __data_columns
    global __model

    with open("source/model/ml.pkl",'rb') as model_file :
        __model = pickle.load(model_file)

    with open("source/model/columns.json","r") as f :
        __data_columns = json.load(f)['data_columns']
        __location = __data_columns[4:]
    
    
def predict_price(input_data):
    """
    Function predicts the price with input data.
    :param property-type: property type data
    :param zip-code: postcode data
    :param area: area(in sq.metre)
    :param rooms: number of rooms
    :return: predicted price value
    """
    load_files()
    #loc_index = np.where(X.columns == input_data['zip-code'])[0]
    #prop_type_index = np.where(X.columns == input_data['property-type'])[0]
    try :
        loc_index = __data_columns.index(str(input_data['zip_code']))
    except :
        loc_index = -1

    try :
        prop_type_index = __data_columns.index(input_data['property-type'])
    except :
        prop_type_index = -1

    x = np.zeros(len(__data_columns))
    x[1] = input_data['rooms_number']
    x[0] = input_data['area']

    if prop_type_index >= 0:
        x[prop_type_index] = 1
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)

#retj = {
#            "area": 200,
#            "property-type": 'APARTMENT',
#            "rooms-number": 3,
#            "zip-code": 1000
#                 }
#retj1 = {
#            "area": 100,
#            "property-type": 'HOUSE',
#            "rooms-number": 2,
#            "zip-code": 4000
#                 }
#
#print(predict_price(retj1))

