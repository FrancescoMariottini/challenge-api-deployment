
from base import Session, engine, Base
from property_data import PropertyData
import pandas as pd
import sys


def get_all():
    return pd.read_sql_table('property_data', engine) 

def insert(df_scrapping):
    columns_duplicates_check = ["postcode", "house_is", "property_subtype", "price", "rooms_number", "area"]
    df_database = pd.read_sql_table('property_data', engine) 
        
    df_final = pd.concat([df_database, df_scrapping])
    df_final = df_final.drop_duplicates(subset=columns_duplicates_check)
    df_final = df_final.drop_duplicates(subset='id')
    try:
        df_final.to_sql('property_data', engine, if_exists='replace')
        return 'Data posted'
    except:
        return sys.exc_info()

