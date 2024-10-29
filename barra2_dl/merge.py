"""
This module contains the barra2 merge function(s).
"""
import pandas as pd

from pathlib import Path


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

    # instantiate dataframe for combined csv results
    df_combined = pd.DataFrame()

    for file in Path(filein_folder).glob(filename_pattern):
        print(f"Merging file: {file}")
        if df_combined.empty:
            # read csv file without indexing to retain time as column for join
            df_combined = pd.read_csv(file)
        else:
            # read next file into new df
            df_add = pd.read_csv(file)
            df_combined = pd.merge(df_combined, df_add, how='outer', on=index_for_join)
            df_combined = merge_suffix_columns(df_combined)

    return df_combined


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

    pass
