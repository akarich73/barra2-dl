"""
General helper functions for barra2-dl.
"""

import pandas as pd

from typing import List


def list_months(start_datetime: str, end_datetime: str, freq: str = 'MS') -> list:
    """Generate list of months from input start and end datetime for url file loop.

    Args:
        start_datetime: str or datetime-like, Left bound for generating dates.
        end_datetime: str or datetime-like, Left bound for generating dates.
        freq: Frequency string representing the interval between dates (default is 'MS').

    Returns:
        list: List of dates from start to end at the given frequency.

    Raises:
        ValueError: If the provided start_datetime or end_datetime are not valid datetime-like.
    """
    try:
        pd.to_datetime(start_datetime)
        pd.to_datetime(end_datetime)
    except ValueError as e:
        raise ValueError("Invalid date(s) provided: {}".format(e))

    df_to_list = pd.date_range(start=start_datetime, end=end_datetime, freq=freq).tolist()
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




