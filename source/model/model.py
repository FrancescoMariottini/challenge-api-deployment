
# import created modules
import modeling as modeling
import evaluation as evaluation

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

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

from tabulate import tabulate
#below two packages are for feature selection
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel


#['source','land_surface', 'facades_number', 'swimming_pool_has','postcode_median_price',
#              'property_subtype_median_facades_number', 'building_state_agg_median_price']
NUM_CV_FOLDS = 3
DEGREE_MAX = 3

def get_linear_modem(df: pd.DataFrame):
    # Drop features which are not relevent
    df = df.drop(['source', 'land_surface', 'swimming_pool_has'], axis=1)
    # postcode_stats contains the no. of properties in each postcode
    postcode_stats = df['postcode'].value_counts(ascending=False)
    #Any location having less than 10 data points should be tagged as "9999" location.
    #This way number of categories can be reduced by huge amount.
    #Later on when we do one hot encoding, it will help us with having fewer dummy columns
    postcode_value_less_than_10 = postcode_stats[postcode_stats <= 10]
    postcode_value_less_than_10
    df['postcode'] = df['postcode'].apply(lambda x: '9999' if x in postcode_value_less_than_10 else x)
    #Drop the features which are irrelevant as per chi - square
    # Use One Hot Encoding For postcodes
    dummies = pd.get_dummies(df, prefix='', prefix_sep='')
    df = dummies.drop(['9999' ], axis='columns')
    X = df.drop(['price'], axis='columns')
    y = df.price
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    # Returns a linear regression model fitted with Ordinary Least Squares method
    lin_reg = modeling.OLS_linear_regression(X_train, y_train)
    return lin_reg










