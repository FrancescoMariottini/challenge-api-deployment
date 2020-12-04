
# import created modules
import modeling
import evaluation

# import standard libraries
import os
import numpy as np
import pandas as pd
import scipy.stats as stats

#import scikit modules
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from typing import List
from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

from tabulate import tabulate
#below two packages are for feature selection
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel

#import pickle to save the model
import pickle
import json

#['source','land_surface', 'facades_number', 'swimming_pool_has','postcode_median_price',
#              'property_subtype_median_facades_number', 'building_state_agg_median_price']

FEATURES = [""]
NUM_CV_FOLDS = 3
DEGREE_MAX = 3

OTHER_BUILDING_SUBTYPES = ["OTHER_PROPERTY", "MIXED_USE_BUILDING"]
FEATURES = ["area", "house_is", "rooms_number", "postcode"]
TARGET = "price"
TRAINING_TO_INPUT_COLUMNS = {"postcode":"zip-code", "is_house":"property-type",
                             "rooms_number":"rooms-number"}

def get_linear_modem(df: pd.DataFrame,
                     features: List[str] = FEATURES,
                     training_to_input_columns : Dict[str, str] = TRAINING_TO_INPUT_COLUMNS,
                     other_building_subtypes : List[str] = OTHER_BUILDING_SUBTYPES,
                     target: str = TARGET):
    # postcode_stats contains the no. of properties in each postcode
    postcode_stats = df['postcode'].value_counts(ascending=False)
    #Any location having less than 10 data points should be tagged as "9999" location.
    #This way number of categories can be reduced by huge amount.
    #Later on when we do one hot encoding, it will help us with having fewer dummy columns
    postcode_value_less_than_10 = postcode_stats[postcode_stats <= 10]
    df['postcode'] = df['postcode'].apply(lambda x: '9999' if x in postcode_value_less_than_10 else x)
    df['house_is'] = df['house_is'].apply(lambda x: "APARTMENT" if x == False else "HOUSE")
    df.loc[df['property_subtype'].isin(other_building_subtypes),"house_is"] = "OTHERS"
    #Drop the features which are irrelevant as per chi - square
    features.append(target)
    df = df.loc[:, features]
    # Use One Hot Encoding For postcodes
    dummies = pd.get_dummies(df, prefix='', prefix_sep='')
    #AH
    df = dummies.drop(['9999', 'OTHERS'], axis='columns')
    df.rename(columns= training_to_input_columns, inplace=True)
    X = df.drop([TARGET], axis='columns')
    y = df.price
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    # Returns a linear regression model fitted with Ordinary Least Squares method
    lin_reg = modeling.OLS_linear_regression(X_train, y_train)
    # save model through pickle
    with open('ml.pkl', 'wb') as model_pkl:
        pickle.dump(lin_reg, model_pkl)
        #
    columns = {'data_columns': [col for col in X.columns]}
    with open("columns.json", "w") as f:
        f.write(json.dumps(columns))
    return lin_reg


lin_reg = get_linear_modem(pd.read_csv("df_after_cleaning.csv"))







