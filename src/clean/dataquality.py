import pandas
import re  # to extract variable type as string from type class

_METHODS = ["duplicates", "null"]


class DataQuality:  # initialise the dq process by importing a table and setting up the main parameters
    def __init__(self, table, methods=None):
        if methods is None:
            methods = _METHODS
        if isinstance(table, pandas.DataFrame):  # import table into class as dataframe
            self.df = table
        elif isinstance(table, dict):  # convert dictionary into dataframe if needed
            self.df = pandas.DataFrame(table)
        else:
            raise Exception("Provided table is neither a dictionary nor a dataframe")
        if all([method in _METHODS for method in methods]):
            self.methods = methods
        else:
            raise Exception("Not all requested methods are available")
        self.flagged, self.description = self.__self_or_none__(dataframe=self.df)  # initialise dataframes in the class
        count_max = max(self.description.loc["count", :].values)
        self.unique_identifiers = []
        for column in self.df.columns:  # based on count_max the columns used to identify the duplicates are appended in a list
            if column != self.df.columns[0] and self.description.loc["count", column] >=  0.5 * count_max:
                self.unique_identifiers.append(column)

    def __self_or_none__(self, dataframe=None):  # initialise the dq dataframes or recovering previous ones
        if not isinstance(dataframe, pandas.DataFrame):
            flagged = self.flagged
        elif isinstance(dataframe, pandas.DataFrame):
            flagged = dataframe.copy(deep=True)  # Flagged df
        description = flagged.replace(
            {False: int(0), True: int(1), "No": int(0), "Yes": int(1), "None": None}).describe(
            # T/F converted into 0/1 before calculating statistical parameters
            include='all',
            percentiles=[0.05, 0.5, 0.95])  # percentile 0.05 and 0.95 more relevant to identify possible outliers
        description = description.append(self.df.dtypes.rename("dtypes"),
                                         ignore_index=False)  # column data types added to the description dataframe
        return flagged, description

    def __check_with_headers__(self, values_to_check,
                               dataframe: pandas.DataFrame):  # check if provided list/dictionary values are in the dataframe columns
        if isinstance(values_to_check, dict):
            values_to_check = values_to_check.keys()
        elif isinstance(values_to_check, list):
            values_to_check = values_to_check
        else:
            raise Exception("Provided values(s) neither a list nor a dictionary")
        if any([key not in dataframe.columns for key in values_to_check]):
            raise Exception("Provided values(s) not in the table headers")

    def flag(self, df=None):  # flag the dataframe for errors
        flagged, description = self.__self_or_none__(df)
        if "duplicates" in self.methods:
            flagged["duplicates"] = flagged.duplicated(
                subset=self.unique_identifiers).replace(
                {True: 1, False: 0})  # find duplicates based on previously defined identifiers (columns)
        if "null" in self.methods:
            flagged["null"] = flagged.isnull().sum(axis=1)  # count the number of null per row
        if df is None:
            self.flagged = flagged
        return flagged

    def describe(self, df=None):  # provide a new description for the dataframe or recover a previous one
        flagged, description = self.__self_or_none__(df)
        if df is None:
            self.description = description
        return description

    def clean(self, df=None):  # clean the dataframe for duplicates, completely empty rows removed within other modules
        flagged, description = self.__self_or_none__(df)
        cleaned = flagged.copy(deep=True).loc[:, description.columns]  # use only non-flagging part of the flagged df
        if "duplicates" in flagged.columns:
            id_column = flagged.columns[0]
            unique_id = flagged.loc[flagged.duplicates == 0, id_column]  # get identifies for unique rows
            cleaned = cleaned[cleaned[id_column].isin(unique_id)]
        if df is None:
            self.description = description
        return cleaned

    def values_format(self, columns_dtypes: dict, df=None,
                      fill_empty=None):  # format values based on provided dictionary
        if not isinstance(df, pandas.DataFrame):
            df = self.df
        self.__check_with_headers__(values_to_check=columns_dtypes, dataframe=df)

        def dtype_change(value, column, dtype_requested):
            if value is None or value == "" or value != value:  # filling null values
                value = fill_empty
            else:  # return ignore nan or none values as they are
                m = re.search("<class '(?P<t>\w+)'>",
                              str(type(value)))  # extract variable type as string from type class
                type_current = m.group('t')
                if type_current != dtype_requested:
                    if isinstance(value, str):
                        if dtype_requested == "int" and value.isnumeric():
                            value = int(value)
                        elif dtype_requested == "float" and value.isdecimal():
                            value = float(value)
                        elif dtype_requested == "yn":
                            if (value == "1") or (value == "True"):
                                value = "Yes"
                            elif (value == "0") or (value == "False"):
                                value = "No"
                    elif isinstance(value, bool):
                        if dtype_requested == "yn":
                            if value:
                                value = "Yes"
                            elif not value:
                                value = "No"
                    elif isinstance(value, int) and dtype_requested == "float":
                        value = float(value)
                    elif isinstance(value, float) and dtype_requested == "int" and value.is_integer():
                        value = int(value)
                    elif dtype_requested == "str":
                        value = str(value)
                    else:
                        raise Exception(
                            r"{} {} {} not converted into {}".format(column, type_current, str(value), dtype_requested))
            return value

        for column, column_dtype in columns_dtypes.items():  # convert dataframe based on dictionary
            df.loc[:, column] = df.loc[:, column].apply(lambda x: dtype_change(x, column, column_dtype))

        df = df.fillna(value=fill_empty)  # filling empty elements

        return df
