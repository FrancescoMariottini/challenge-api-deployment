import pickle
import numpy as np
import json
import csv
from sklearn.linear_model import LinearRegression

__location = None
__data_columns = None
__model = None
__metrics = None

#dynamic filepahts for win testing (FM)
import os
MODEL_FOLDER = os.path.join(os.path.dirname(os.getcwd()), "model")
#MODEL_FOLDER = "src/model"


def load_files(model_subtype: str = "OTHERS"):

    global __data_columns
    global __model
    MODEL_SUBTYPES = ["APARTMENT", "HOUSE", "OTHERS"]

    if model_subtype not in MODEL_SUBTYPES:
        model_subtype = "OTHERS"

    with open(MODEL_FOLDER+"/"+model_subtype.lower()+".pkl", 'rb') as model_file :
        __model = pickle.load(model_file)

    with open(MODEL_FOLDER+"/"+model_subtype.lower()+".json","r") as f :
        __data_columns = json.load(f)['data_columns']

    with open(MODEL_FOLDER + "/" + "models_metrics.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)
    
    
def predict_price(input_data):
    """
    Function predicts the price with input data.
    :param property-type: property type data
    :param zip-code: postcode data
    :param area: area(in sq.metre)
    :param rooms: number of rooms
    :return: predicted price value
    """
    
    load_files(input_data['property_type'])
    
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
    x[1] = input_data['rooms-number']
    x[2] = input_data["land-area"]
    x[3] = input_data["garden"]
    x[4] = input_data["garden-area"]
    x[5] = input_data["equipped-kitchen"]
    x[6] = input_data["swimmingpool"]
    x[7] = input_data["furnished"]
    x[8] = input_data["open-fire"]
    x[9] = input_data["terrace"]
    x[10] = input_data["terrace-area"]
    x[11] = input_data["facades-number"]

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
"property_type": "HOUSE",
"rooms_number": 3,
"zip_code": 8300,
"land_area": 500,
"garden": 1,
"garden_area": 50,
"equipped_kitchen": 0,
"swimmingpool": 0,
"furnished": 1,
"open_fire": 0,
"terrace": 1,
"terrace_area": 10,
"facades_number": 3,
"building_state": "GOOD"
}

#testing
print(predict_price(retj))
