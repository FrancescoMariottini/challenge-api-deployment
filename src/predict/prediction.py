import pickle
import numpy as np
import json
import csv
from sklearn.linear_model import LinearRegression
#import joblib

__location = None
__data_columns = None
__model = None

def load_files(model_subtype: str = "OTHERS"):
    
    global __data_columns
    global __model
    MODEL_SUBTYPES = ["APARTMENT", "HOUSE", "OTHERS"]

    if model_subtype not in MODEL_SUBTYPES:
        model_subtype = "OTHERS"

    with open("src/model/"+model_subtype.lower()+".pkl", 'rb') as model_file :
        __model = pickle.load(model_file)
  
    with open("src/model/"+model_subtype.lower()+".json","r") as f :
        __data_columns = json.load(f)['data_columns']
        
    ##loading file to be completed
    with open(MODEL_FOLDER + "/" + "models_metrics.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)
            #if filename is according to model retrieve metrics
    
    
    
    
def predict_price(input_data):
    """
    Function predicts the price with input data.
    :param property-type: property type data
    :param zip-code: postcode data
    :param area: area(in sq.metre)
    :param rooms: number of rooms
    :return: predicted price value
    """
    
    load_files(input_data['property-type'])
    
    input_data['log_area'] = np.log(input_data['area'])
    log_on_columns = ["garden_area", "terrace_area", "land_area", "area"]

    for c in log_on_columns:
        # input_data[c] = input_data[c].apply(np.log)
        input_data[c] = np.log(input_data[c])

    try :
        loc_index = __data_columns.index(str(input_data['zip_code']))
    except :
        loc_index = -1

    '''try :
        prop_type_index = __data_columns.index(input_data['property-type'])
    except :
        prop_type_index = -1
    '''

    try :
        prop_state_index = __data_columns.index(input_data["building_state"])
    except :
        prop_state_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = input_data['area']
    x[1] = input_data['rooms_number']
    x[2] = input_data["land_area"]
    x[3] = input_data["garden"]
    x[4] = input_data["garden_area"]
    x[5] = input_data["equipped_kitchen"]
    x[6] = input_data["swimmingpool"]
    x[7] = input_data["furnished"]
    x[8] = input_data["open_fire"]
    x[9] = input_data["terrace"]
    x[10] = input_data["terrace_area"]
    x[11] = input_data["facades_number"]

    '''
    if prop_type_index >= 0:
        x[prop_type_index] = 1
        '''
    if loc_index >= 0:
        x[loc_index] = 1
    if prop_state_index >= 0:
        x[prop_state_index] = 1

    
    return round((__model.predict([x])[0]), 2)

retj = {
"area": 300,
"property-type": "HOUSE",
"rooms-number": 3,
"zip-code": 8300,
"land-area": 500,
"garden": 1,
"garden-area": 50,
"equipped-kitchen": 0,
"swimmingpool": 0,
"furnished": 1,
"open-fire": 0,
"terrace": 1,
"terrace-area": 10,
"facades-number": 3,
"building-state": "GOOD"
}

#print(predict_price(retj))
