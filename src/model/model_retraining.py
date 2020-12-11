#import necessary libraries
from scraping import scraping
from preprocessing_dataset import clean_for_database 
import models_creation
from dataset.repository import insert
import typing
import pandas as pd
from preprocess_features import preprocess_features

def train(): 

    # Initiating the scraping function
    results: list = scraping.get_search_results(minresults:int)
    new_data : dict = scraping.scrap_list(results)

    # call the data cleaning function
    df, df_outliers = clean_for_database(new_data)

    # establish connection with the database
    #check if the conn id established

    # call the update_database function

    message = insert(df)
    df_out = get_all()
    
    if message = 'Data posted' :
        # call the preprocess for features
        df_out = preprocess_features(df_out)        
        # call the model function
        status = models_creation.get_linear_model(df_out)
    else : 
        status = message
    
    return status

