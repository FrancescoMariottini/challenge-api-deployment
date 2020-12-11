import pandas as pd
import numpy as np
from typing import List
from typing import Dict

TARGET = "price"
OTHER_PROPERTY_SUBTYPES = ["OTHER_PROPERTY", "MIXED_USE_BUILDING"]
LOG_ON_COLUMNS = ["garden_area", "terrace_area", "land_surface", "area"]
#defining allowed model subtypes
MODEL_SUBTYPES = ["APARTMENT", "HOUSE", "OTHERS"]

def preprocess_features(df_out: pd.DataFrame = None,
                        features: List[str] = None,
                        target: str = TARGET,
                        model_subtype: str = "OTHERS",
                        other_property_subtypes: List[str] = OTHER_PROPERTY_SUBTYPES,
                        log_on_columns: List[str] = LOG_ON_COLUMNS):
    # preprocessing after database
    # FM 7/12/20 filtering dataframe before hot encoding
    # postcode_stats contains the no. of properties in each postcode
    postcode_stats = df_out['postcode'].value_counts(ascending=False)
    # Any location having less than 10 dataset points should be tagged as "9999" location.
    # This way number of categories can be reduced by huge amount.
    # Later on when we do one hot encoding, it will help us with having fewer dummy columns
    postcode_value_less_than_10 = postcode_stats[postcode_stats <= 10]
    df_out['postcode'] = df_out['postcode'].apply(lambda x: '9999' if x in postcode_value_less_than_10 else x)
    df_out['house_is'] = df_out['house_is'].apply(lambda x: "APARTMENT" if x == False else "HOUSE")
    df_out.loc[df_out['property_subtype'].isin(other_property_subtypes), "house_is"] = "OTHERS"
    if model_subtype not in MODEL_SUBTYPES:
        print(f'{model_subtype} model not found, OTHERS model used. Available models are:')
        print(",".join([m for m in MODEL_SUBTYPES]))
        model_subtype = "OTHERS"
    df_out = df_out.loc[df_out['house_is'] == model_subtype, :]
    # keep only the features which are irrelevant as per chi - square
    features.append(target)
    df_out = df_out.loc[:, features]
    for c in log_on_columns:
        df_out[c] = df_out[c].replace(to_replace=0, value=1)
        df_out[c] = df_out[c].apply(np.log)
    return df_out