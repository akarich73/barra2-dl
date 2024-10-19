"""
This module contains the barra2 merge function(s).
"""
from pathlib import Path
import pandas as pd
import fnmatch


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


def merge_csvs_to_df(filein_folder: str,
                    filename_pattern: str = '*.csv',
                    index_for_join: str = None) -> pd.DataFrame:
    """
    Function to merge csv files iteratively from a folder based on filename wildcard.
    If filename wildcard is omitted all csv files in the folder will be merged.

    Args:
        filein_folder (str): Optional
        filename_pattern (str):
        index_for_join (str):

    Returns:
        DataFrame: A DataFrame with the merged csvs.

    Todo:
        add .csv check for filename_prefix
    """

    def merge_suffix_columns(df: pd.DataFrame, suffix_x: str = '_x', suffix_y: str = '_y') -> pd.DataFrame:
        """
        Function to merge DataFrame columns with '_x' and '_y' suffixes.

        Args:
            df: The DataFrame that contains columns with suffixes to be merged.
            suffix_x: The suffix used in the first set of columns (default is '_x').
            suffix_y: The suffix used in the second set of columns (default is '_y').

        Returns:
            DataFrame: A DataFrame with the merged columns.
            If no suffix_x returns the original DataFrame.

        Todo:
            Add checks for multiple and mismatched suffixed columns
        """
        for column in df.columns:
            if column.endswith(suffix_x):
                base_column = column[:-len(suffix_x)]
                column_y = base_column + suffix_y
                if column_y in df.columns:
                    # Create a new column without suffix and merge the values
                    df[base_column] = df[column].combine_first(df[column_y])
                    # Drop the old suffix columns
                    df.drop([column, column_y], axis=1, inplace=True)
        return df

    # initiate dataframe for combined csv results
    df_combined = pd.DataFrame()

    for file in Path(filein_folder).glob(filename_pattern):
        print(f"Merging file: {file}")
        if df_combined.empty:
            # read csv file without indexing to retain time as column for join
            df_combined = pd.read_csv(file)
        else:
            # read next file into new df
            df_add = pd.read_csv(file)
            # combine on index join if not None, otherwise just concat together
            # todo df_combined = df1.merge(df2,how='outer') seems to guess the matching columns
            df_combined = pd.merge(df_combined, df_add, how='outer', on=index_for_join)
            df_combined = merge_suffix_columns(df_combined)

    return df_combined



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


def export_df_to_csv(dataframe: pd.DataFrame,
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
