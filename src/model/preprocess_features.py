import pandas as pd
import numpy as np
from typing import List
from typing import Dict

TARGET = "price"
FEATURES = ["area", "rooms_number", "postcode",'land_surface','garden','garden_area','equipped_kitchen_has',
            'swimming_pool_has','furnished','open_fire', 'terrace', 'terrace_area', 'facades_number','building_state_agg']
OTHER_PROPERTY_SUBTYPES = ["OTHER_PROPERTY", "MIXED_USE_BUILDING"]
LOG_ON_COLUMNS = ["garden_area", "terrace_area", "land_surface", "area"]
#defining allowed model subtypes
MODEL_SUBTYPES = ["APARTMENT", "HOUSE", "OTHERS"]

# e.g. distinction between old and new buildings
COLUMNS_GROUPED_BY = {"facades_number": "property_subtype"} #not neeeded by Ankita: "price":"property_subtype", "price":"region"}  "price":"building_state_agg"}
COLUMNS_TO_REPLACE = ["facades_number"]
GROUPBY_AGGREGATORS = [np.median]  # [min,max,np.mean,np.median,len]
AGGREGATOR_COLUMNS = {min: "min", max: "max", np.mean: "mean", np.median: "median", len: "len"}



# 11/12/20 dropping transfered to features if needed (should happen in dataset)
# self.df_out, index_dropped = self.drop_duplicates()
# fill nan after replacing facades_number with grouping to avoid modelling issues
# self.df_out = self.fill_na(self.df_out)
# print(f"{len(index_dropped)} Dropped duplicates, shape: {self.df_out.shape}")

def add_aggregated_columns(df: pd.DataFrame, group_parameters: Dict[str, str] = COLUMNS_GROUPED_BY,
                          groupby_aggregators: List = GROUPBY_AGGREGATORS,
                          columns_to_replace: List[str] = None) -> (pd.DataFrame, List[str]):
    """
    Create aggregated columns to deal with missing values and non-numerical values
    :param df: input table
    :param group_parameters: parameter and column to group for.
    :param groupby_aggregators: aggregate function to use
    :param columns_to_replace: original columns to be replaced with grouped values
    :return df: dataframe with new aggregated columns
    :return column_names: names of added aggregated columns
    """
    aggregated_column_names = []
    column_names = []
    for key, value in group_parameters.items():
        #dealing with null when grouping
        if not df.loc[:, key].isnull().all():
            try:
                df_grp = df.loc[:, [key, value]].dropna(axis=0).groupby(value, as_index=False)[key].agg(groupby_aggregators)
                column_names = [f"{value}_{AGGREGATOR_COLUMNS[aggregator]}_{key}" for aggregator in groupby_aggregators]
                df = df.merge(df_grp, on=value, how='left')
                aggregated_column_names += column_names
                df.rename(columns=dict(zip([AGGREGATOR_COLUMNS[aggregator] for aggregator in groupby_aggregators], column_names)), inplace=True)
            except pd.core.base.DataError:
                columns_to_replace.remove(key)
                print(f'aggregation not working for {key}')
        # drop at the end so order in group_parameters not important
        else:
            #remove columns could not regroup
            if value in columns_to_replace:
                columns_to_replace.remove(key)
                print(f'Only null values for {key}')
    if columns_to_replace is not None:
        df.drop(labels=[c for c in columns_to_replace], axis=1, inplace=True)
        if "facades_number" in columns_to_replace:
            df.rename(columns={'property_subtype_median_facades_number': "facades_number"}, inplace=True) #24/11/20 fast fix
    return df, column_names

def preprocess_features(df_out: pd.DataFrame = None,
                        features: List[str] = FEATURES,
                        target: str = TARGET,
                        model_subtype: str = "OTHERS",
                        other_property_subtypes: List[str] = OTHER_PROPERTY_SUBTYPES,
                        log_on_columns: List[str] = LOG_ON_COLUMNS):
    # aggregation to deal with many nan in facades_number
    # 11/12/20 aggregation transfered to features since values may be missed
    df_out, aggregated_column_names = add_aggregated_columns(df_out, columns_to_replace=COLUMNS_TO_REPLACE)
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
    # replacing bool to avoid scikit-learn issue later #moved from preprocessing on 11/12/20
    df_out = df_out.replace(to_replace=[True, False], value=[1, 0])
    return df_out