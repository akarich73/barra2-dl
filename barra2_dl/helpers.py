"""
This module contains helper functions.
"""

import pandas as pd
import fnmatch
from pathlib import Path
from typing import List


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


def list_csv_files(folder_path):
    """
    List all CSV files in the given folder.

    Args:
        folder_path (str): The path to the folder containing the CSV files.

    Returns:
        list: A list of CSV file names in the folder.
    """
    folder = Path(folder_path)
    csv_files = [file.name for file in folder.glob('*.csv')]
    return csv_files


def filter_list_using_wildcard(input_list: list[str], pattern:str):
    """
    Filter a list using a wildcard pattern.

    Args:
        input_list (list[str]): The list of strings to be filtered.
        pattern (str): The wildcard pattern to filter the list.

    Returns:
        list: A list of strings that match the wildcard pattern.
    """
    filtered_list = fnmatch.filter(input_list, pattern)
    return filtered_list


def merge_csv_files_to_dataframe(filein_folder: str,
                    filename_pattern: str = '*.csv',
                    index_for_join: str = None) -> pd.DataFrame:
    """
    Merge csv files from a folder based on optional filename wildcard using fnmatch.
    If filename wildcard is omitted all csv files in the folder will be merged.
    If fileout_folder is omitted the merged file will be saved in the filein_folder.

    Args:
        filein_folder (str): Optional
        filename_pattern (str):
        index_for_join (str):

    Returns:
        return_type: None.

    Todo:
        Change from using os to pathlib
    """

    # todo add .csv check for filename_prefix


    # list all csv files in folder
    csv_files = list_csv_files(filein_folder)

    # filter csv files
    csv_files_filtered = filter_list_using_wildcard(csv_files, filename_pattern)

    # initiate dataframe for combined csv results
    df_combined = pd.DataFrame()

    for file in Path(filein_folder).glob(filename_pattern):
        if df_combined.empty:
            # read csv file without indexing to retain time as column for join
            df_combined = pd.read_csv(file)
        else:
            # read next file into new df
            df_add = pd.read_csv(file)
            # combine on index join if not None, otherwise just concat together
            if index_for_join is not None:
                df_combined = df_combined.join(df_add.set_index(index_for_join),on=index_for_join)
            else:
                df_combined = pd.concat([df_combined, df_add], ignore_index = True)

    return df_combined


def export_dataframe_to_csv(dataframe: pd.DataFrame,
                            fileout_folder: str | Path,
                            fileout_name: str,
                            create_folder: bool = True) -> None:
    """
    Export a DataFrame to a CSV file in the specified folder with the given file name.

    Args:
        dataframe (pd.DataFrame): The Pandas DataFrame to export.
        fileout_folder (str or Path): The path to the folder where the CSV file will be saved.
        fileout_name (str): The name of the CSV file to save.
        create_folder (bool): If True, creates the folder if it does not exist; otherwise, exits if the folder doesn't exist.

    Returns:
        Path: The path of the saved CSV file.
    """
    fileout_folder = Path(fileout_folder)
    # Check if the folder exists
    if not fileout_folder.exists():
        if create_folder:
            fileout_folder.mkdir(parents=True)
            print(f"The folder '{fileout_folder}' was created.")
        else:
            print(f"The folder '{fileout_folder}' does not exist. Exiting...")
            return

    # Define the full path for the CSV file
    fileout_path_name = fileout_folder / fileout_name

    # Export the DataFrame to CSV
    dataframe.to_csv(fileout_path_name, index=False)

    return fileout_path_name


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
