"""
General helper functions for barra2-dl.
"""

import pandas as pd
from typing import List, Union


def list_months(start_datetime: str, end_datetime: str, freq: str ='MS', **kwargs) -> list:
    """Generate list of months from input start and end datetime for url file loop.

    Args:
        freq:
        start_datetime: str or datetime-like, Left bound for generating dates.
        end_datetime: str or datetime-like, Left bound for generating dates.
        **kwargs:

    Returns:
        list
    """
    df_to_list = pd.date_range(start=start_datetime, end=end_datetime, freq=freq, **kwargs).tolist()
    return df_to_list


def get_timestamp_range_list(dataframe: pd.DataFrame, timestamp_column: str) -> List[pd.Timestamp]:
    """
    Get a list containing the range between the first and last timestamp in the specified column of the DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the timestamp column.
        timestamp_column (str): The name of the timestamp column in the DataFrame.

    Returns:
        list: A list containing the first and last timestamp.
    """
    if timestamp_column not in dataframe.columns:
        raise ValueError(f"Column '{timestamp_column}' does not exist in the DataFrame.")

    # Ensure the column is of datetime type
    dataframe[timestamp_column] = pd.to_datetime(dataframe[timestamp_column])

    # Sort the DataFrame by the timestamp column
    dataframe = dataframe.sort_values(by=timestamp_column)

    # Get the first and last timestamp
    first_timestamp = dataframe[timestamp_column].iloc[0]
    last_timestamp = dataframe[timestamp_column].iloc[-1]

    return [first_timestamp, last_timestamp]




