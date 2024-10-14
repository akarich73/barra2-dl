"""
This module contains the barra2 download function(s) .
"""
import requests
from datetime import datetime, timedelta
from pathlib import Path
import calendar
from .helpers import list_months
from .globals import LatLonPoint, LatLonBBox, barra2_index


def download_file(url: str,
                  folder_path: str | Path,
                  file_name: str,
                  create_folder: bool = False) -> None:
    """Download the file from the url and saves it as folder_path/filename.
    If the downloads folder does not exist, it will be created due to the create_folder=True argument.
    Args:
        url: The URL of the file to be downloaded.
        folder_path: The path where the file should be saved.
        file_name: The name to save the downloaded file as.
        create_folder: If True, creates the folder if it does not exist; otherwise, exits if the folder doesn't exist.
    Returns:
        None
    """
    folder = Path(folder_path)
    file = folder / file_name

    # Check if the folder exists
    if not folder.exists():
        if create_folder:
            folder.mkdir(parents=True)
            print(f"The folder '{folder_path}' was created.")
        else:
            print(f"The folder '{folder_path}' does not exist. Exiting...")
            return

    # Check if the file already exists
    if file.exists():
        print(f"The file '{file_name}' already exists in the folder '{folder_path}'.")
    else:
        # Download the URL to the file
        response = requests.get(url)
        file.write_bytes(response.content)
        print(f"File '{file_name}' has been downloaded to '{folder_path}'.")

    return


def barra2_point_downloader(base_url: str,
                            barra2_var: list,
                            lat_lon_point: LatLonPoint,
                            start_datetime: str | datetime,
                            end_datetime: str | datetime,
                            fileout_prefix: str,
                            fileout_folder: str = 'cache',
                            fileout_type: str = 'csv_file') -> None:
    """Download barra2 data based on the url and variables list
    for each month between start and end datetime.

    Args:
        base_url (str): Use from barra2-dl.globals or set explicitly
        barra2_var (list): Use from barra2-dl.globals or set explicitly
        lat_lon_point (LatLonPoint: TypedDict): Use custom class for barra2-dl.globals or as Dict{'lat':float, 'lon':float}
        start_datetime (str | datetime): Used to define start of inclusive download period
        end_datetime (str | datetime): Used to define end of inclusive download period
        fileout_prefix (str): Optional prefix for downloaded file. E.g. location reference.
        fileout_folder (str): Relative or absolute path for downloaded files
        fileout_type (str): Output file option, 'csv_file'

    Returns:
        Downloaded files into fileout_folder as f'{fileout_prefix}_{var}_{time_start[:10]}_{time_end[:10]}.csv'

    Todo:
        Add set list of output format options
        Change from using os to pathlib

    """

    # loop through each variable requested for download as each variable is saved in a separate url
    for var in barra2_var:
        # loop through each month as each BARRA2 file is saved by month
        for date in list_months(start_datetime, end_datetime, freq="MS"):
            year = date.year
            month = date.month
            time_start = date.isoformat() + 'Z'
            # Get the number of days in the current month
            days_in_month = calendar.monthrange(year, month)[1]
            time_end = (date + timedelta(days=days_in_month) + timedelta(hours=-1)).isoformat() + 'Z'

            # update thredds_base_url and set as url for request
            url = base_url.format(var=var, year=year, month=month)

            # add url parameters to base_url
            url += f"?var={var}&latitude={lat_lon_point['lat']}&longitude={lat_lon_point['lon']}&time_start={time_start}&time_end={time_end}&accept={fileout_type}"
            fileout_name = f'{fileout_prefix}_{var}_{time_start[:10]}_{time_end[:10]}.csv'
            folder_path = fileout_folder
            download_file(url, folder_path, fileout_name, create_folder=True)

    return




