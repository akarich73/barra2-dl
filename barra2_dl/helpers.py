"""
General helper functions.
"""

from pathlib import Path
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

# # todo draft function to process csvs
# def process_csvs:
#       # process barra2 variables to wind speed and direction todo split into modules
#
#     # initiate DataFrame for adding new columns
#     df_processed = df_combined
#
#     # loop through df_combined to df_processed
#     for tup in barra2_wind_speeds:
#         mask_wind_speed_h = tup[0][2:]
#         mask_ua = df_combined.columns.str.contains(tup[0])  # selects column header
#         mask_va = df_combined.columns.str.contains(tup[1])  # selects column header
#
#         if np.any(mask_ua == True) and np.any(mask_va == True):
#             df_processed_ua = df_combined.loc[:, mask_ua]  # selects mask
#             df_processed_va = df_combined.loc[:, mask_va]  # selects mask
#
#             print('Converted: ' + tup.__str__())
#
#             df_processed_v = pd.DataFrame(np.sqrt(df_processed_ua.iloc[:, 0] ** 2 + df_processed_va.iloc[:, 0] ** 2))
#             df_processed_v.columns = ['v' + mask_wind_speed_h + '[unit="m s-1"]']
#
#             df_processed_phi_met = pd.DataFrame()
#
#             for index, row in df_combined.iterrows():
#                 if (df_processed_ua.iloc[index, 0] == 0) and (df_processed_va.iloc[index, 0] == 0):
#                     df_processed_phi_met.loc[index, 'v' + mask_wind_speed_h + '_' + 'phi_met[unit="degrees"]'] = 0.0
#                 else:
#                     df_processed_phi_met.loc[index, 'v' + mask_wind_speed_h + '_' + 'phi_met[unit="degrees"]'] = (
#                         np.mod(180 + np.rad2deg(
#                             np.arctan2(df_processed_ua.iloc[index, 0], df_processed_va.iloc[index, 0])), 360))
#
#             # Merge the current variable DataFrame with the combined DataFrame
#             df_processed = df_processed.join(df_processed_v)
#             df_processed = df_processed.join(df_processed_phi_met)
#
#     # export combined to csv
#     df_processed.to_csv(
#         os.path.join(output_dir,
#                      f"{output_filename_prefix}_processed_{start_date_time.strftime("%Y%m%d")}_{end_date_time.strftime("%Y%m%d")}.csv"))
#
#     return



