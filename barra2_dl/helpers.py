"""
This module contains helper functions.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import fnmatch
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

# todo draft function to combine csv files on index need to check and add tests
def combine_csv_files(file_paths: list[str | Path], output_file: str | Path, index_col: str) -> None:
    """
    Combine multiple CSV files with a common index column into a single CSV file.

    Args:
        file_paths (list[str | Path]): A list of file paths to the CSV files to be combined.
        output_file (str | Path): The path where the combined CSV file should be saved.
        index_col (str): The name of the column to be used as the index for combining the CSV files.

    Returns:
        None
    """
    combined_df = None

    for file_path in file_paths:
        # Read the current CSV file
        df = pd.read_csv(file_path, index_col=index_col)

        if combined_df is None:
            combined_df = df
        else:
            combined_df = combined_df.join(df, how='outer')

    # Save the combined DataFrame to the output file
    combined_df.to_csv(output_file)

    return

# todo draft function to process csvs
def process_csvs:
      # process barra2 variables to wind speed and direction todo split into modules

    # initiate DataFrame for adding new columns
    df_processed = df_combined

    # loop through df_combined to df_processed
    for tup in barra2_wind_speeds:
        mask_wind_speed_h = tup[0][2:]
        mask_ua = df_combined.columns.str.contains(tup[0])  # selects column header
        mask_va = df_combined.columns.str.contains(tup[1])  # selects column header

        if np.any(mask_ua == True) and np.any(mask_va == True):
            df_processed_ua = df_combined.loc[:, mask_ua]  # selects mask
            df_processed_va = df_combined.loc[:, mask_va]  # selects mask

            print('Converted: ' + tup.__str__())

            df_processed_v = pd.DataFrame(np.sqrt(df_processed_ua.iloc[:, 0] ** 2 + df_processed_va.iloc[:, 0] ** 2))
            df_processed_v.columns = ['v' + mask_wind_speed_h + '[unit="m s-1"]']

            df_processed_phi_met = pd.DataFrame()

            for index, row in df_combined.iterrows():
                if (df_processed_ua.iloc[index, 0] == 0) and (df_processed_va.iloc[index, 0] == 0):
                    df_processed_phi_met.loc[index, 'v' + mask_wind_speed_h + '_' + 'phi_met[unit="degrees"]'] = 0.0
                else:
                    df_processed_phi_met.loc[index, 'v' + mask_wind_speed_h + '_' + 'phi_met[unit="degrees"]'] = (
                        np.mod(180 + np.rad2deg(
                            np.arctan2(df_processed_ua.iloc[index, 0], df_processed_va.iloc[index, 0])), 360))

            # Merge the current variable DataFrame with the combined DataFrame
            df_processed = df_processed.join(df_processed_v)
            df_processed = df_processed.join(df_processed_phi_met)

    # export combined to csv
    df_processed.to_csv(
        os.path.join(output_dir,
                     f"{output_filename_prefix}_processed_{start_date_time.strftime("%Y%m%d")}_{end_date_time.strftime("%Y%m%d")}.csv"))

    return


# todo add tests
def calculate_wind_speed(u: Union[float, int], v: Union[float, int]) -> float:
    """
    Args:
        u: The u component of the wind vector, which can be a float or an int.
        v: The v component of the wind vector, which can be a float or an int.
    Returns:
        Wind speed. If both u and v are zero, it returns 0.0.
    """
    if u == 0 and v == 0:
        return 0.0
    return np.sqrt(u ** 2 + v ** 2)

def wind_components_to_speed(ua: Union[float, int, List[float], List[int]], va: Union[float, int, List[float], List[int]]) -> Union[float, List[float]]:
    """
    Convert wind components ua and va to wind speed v.
    Args:
        ua (Union[float, int, List[float], List[int]]): The u-component of the wind.
        va (Union[float, int, List[float], List[int]]): The v-component of the wind.
    Returns:
        float or List[float]: The calculated wind speed.
    Raises:
        ValueError: If the input types do not match or if they are neither List[float] nor float.
    """
    if isinstance(ua, (float, int)) and isinstance(va, (float, int)):
        if ua == 0 and va == 0:
            return 0.0
        return calculate_wind_speed(ua, va)
    elif isinstance(ua, list) and isinstance(va, list):
        if not all(isinstance(num, (float, int)) for num in ua + va):
            raise ValueError("All elements in both lists must be either float or int.")
        if len(ua) != len(va):
            raise ValueError("Both lists must be of the same length.")
        return [calculate_wind_speed(u, v) for u, v in zip(ua, va)]
    else:
        raise ValueError("Both arguments must be either both float/int or both lists of float/int.")


# todo add tests
def calculate_wind_direction(u: Union[float, int], v: Union[float, int]) -> float:
    """
    Args:
        u: The u component of the wind vector, which can be a float or an int.
        v: The v component of the wind vector, which can be a float or an int.
    Returns:
        Wind direction in degrees. If both u and v are zero, it returns 0.0.
    """
    if u == 0 and v == 0:
        return 0.0
    return np.mod(180 + np.rad2deg(np.arctan2(u, v)), 360)

def wind_components_to_direction(ua: Union[float, int, List[float], List[int]], va: Union[float, int, List[float], List[int]]) -> Union[float, List[float]]:
    """
    Convert wind components ua and va to wind direction phi.
    Args:
        ua (Union[float, int, List[float], List[int]]): The u-component of the wind.
        va (Union[float, int, List[float], List[int]]): The v-component of the wind.
    Returns:
        float or List[float]: The calculated wind speed.
    Raises:
        ValueError: If the input types and incorrect or do not match or if lists of different lengths are provided.
    """

    if isinstance(ua, (float, int)) and isinstance(va, (float, int)):
        return calculate_wind_direction(ua, va)
    elif isinstance(ua, list) and isinstance(va, list):
        if not all(isinstance(num, (float, int)) for num in ua + va):
            raise ValueError("All elements in both lists must be either float or int.")
        if len(ua) != len(va):
            raise ValueError("Both lists must be of the same length.")
        return [calculate_wind_direction(u, v) for u, v in zip(ua, va)]
    else:
        raise ValueError("Both arguments must be either both float/int or both lists of float/int.")

