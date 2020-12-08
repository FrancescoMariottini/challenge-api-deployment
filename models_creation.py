"""Wrap-up module for models creation"""


# import created modules
import model.modeling as modeling
import model.evaluation as evaluation
from model.preprocessing_dataset import DataCleaning

# import standard libraries
import os
import numpy as np
import pandas as pd

#import scikit modules
from sklearn.model_selection import train_test_split
from sklearn.metrics import median_absolute_error
from sklearn.metrics import max_error

#import typing
from typing import List
from typing import Dict

#import pickle to save the model
import pickle
import json

#FM 8/12/2020 parameters to be checked in Joachim modeml
NUM_CV_FOLDS = 3
DEGREE_MAX = 3

#FM 7/12/20 defining allowed model subtypes
TRAINING_TO_INPUT_COLUMNS = {"postcode":"zip-code", "land_surface":"land-area",
                             "rooms_number":"rooms-number", 'equipped_kitchen_has': "equipped-kitchen",
                             'swimming_pool_has': "swimmingpool" , 'open_fire' : "open-fire" ,
                              'terrace_area' : "terrace-area" , 'facades_number' :"facades-number",
                              'building_state_agg': "building-state", 'garden_area':"garden-area"
                             }

FEATURES = ["area", "rooms_number", "postcode",'land_surface','garden','garden_area','equipped_kitchen_has',
            'swimming_pool_has','furnished','open_fire', 'terrace', 'terrace_area', 'facades_number','building_state_agg',]

TARGET = "price"
MODEL_SUBTYPE = "OTHERS"
LOG_ON_COLUMNS= ["garden_area", "terrace_area", "land_surface", "area"]
#FM 7/12/20 defining dummies to be dropped. Others removed since filtering
DUMMIES_TO_DROP = ['9999', 'to_renovate']


#FM 7/12/20 11:59 updated dynamic filepath following new structure
#FM 8/12/2020 different ways for linux & win really necessary ?
"""DEFAULT VALUES SETUP"""
DATASET_CSV_FILEPATH = os.path.join(os.getcwd(), 'dataset', 'clean_dataset.csv')
MODEL_FOLDER = os.path.join(os.getcwd(), 'src', 'model')
REAL_ESTATE_CSV_FILEPATH = os.path.join(os.getcwd(), 'dataset','clean_dataset.csv')
CLEANED_CSV_FILEPATH = os.path.join(os.getcwd(), 'outputs', 'df_after_cleaning.csv')
#paths for windows users
DATASET_CSV_FILEPATH_WIN = os.getcwd() + r"\dataset" + "\clean_dataset.csv"
MODEL_FOLDER_WIN = os.getcwd() + r"\src" + r"\model"
REAL_ESTATE_CSV_FILEPATH_WIN = os.getcwd() + r"\dataset" + "\clean_dataset.csv"
CLEANED_CSV_FILEPATH_WIN = os.getcwd() + r"\outputs" + "\df_after_cleaning.csv"

def get_linear_model(df: pd.DataFrame,
                     target: str = TARGET,
                     model_subtype: str = "OTHERS", #FM 7/12/20 model subtype added
                     training_to_input_columns : Dict[str, str] = TRAINING_TO_INPUT_COLUMNS,
                     dummies_to_drop: List[str] = DUMMIES_TO_DROP,
                     model_folder: str = MODEL_FOLDER):

    # Use One Hot Encoding For postcodes
    dummies = pd.get_dummies(df, prefix='', prefix_sep='')
    #FM 7/12/20 fixed list of dummies replaced with variable (no drop of OTHERS if filtering)
    df = dummies.drop(dummies_to_drop, axis='columns')
    df.rename(columns= training_to_input_columns, inplace=True)
    X = df.drop([target], axis='columns')
    y = df.price
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    # Returns a linear regression model fitted with Ordinary Least Squares method
    lin_reg = modeling.OLS_linear_regression(X_train, y_train)
    # save model through pickle
    # FM 7/12/20 filename based on model_type
    # FM 7/12/20 lower character really necessary ?
    pkl_filename = model_subtype.lower()+'.pkl'
    with open(os.path.join(model_folder, pkl_filename), 'wb') as model_pkl:
        pickle.dump(lin_reg, model_pkl)
    #FM 8/12/20 Ankita please clarify why needed
    columns = {'data_columns': [col for col in X.columns]}
    json_filename = model_subtype.lower() + '.json'
    with open(os.path.join(model_folder, json_filename), "w") as f:
        f.write(json.dumps(columns))
    #FM 7/12/20  initialising model evalution to get error
    model_evaluation_obj = evaluation.Model_Evaluation(lin_reg)
    ytrain_predictions, ytest_predictions = model_evaluation_obj.get_predictions(X_train, X_test)
    y_test, ytest_predictions, metrics = model_evaluation_obj.predict_model(X_train, y_train, X_test, y_test)
    text_stream = open("models_metrics.csv", 'a')
    #text_stream.write(",".join([pkl_filename]+[m for m in metrics_values]) + "\n")
    return lin_reg, metrics


#TESTING ON WINDOWS (to exclude as comment when running Jupyter NB)

dc = DataCleaning(csv_filepath = REAL_ESTATE_CSV_FILEPATH_WIN)
df, df_outliers = dc.get_preprocessed_dataframe(cleaned_csv_path= CLEANED_CSV_FILEPATH_WIN,
                                                features= FEATURES,
                                                model_subtype= MODEL_SUBTYPE,
                                                log_on_columns= LOG_ON_COLUMNS)
lin_reg, metrics = get_linear_model(df, model_subtype= MODEL_SUBTYPE)
print(metrics)
print(df_outliers)
print(df.info())
#print(describe_with_tukey_fences(df))








