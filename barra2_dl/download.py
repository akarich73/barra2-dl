"""This module contains the barra2 download function(s)."""

import calendar
from datetime import datetime, timedelta
from pathlib import Path

import requests

from barra2_dl.globals import LatLonPoint
from barra2_dl.helpers import list_months


def download_file(
    url: str,
    folder_path: str | Path,
    file_name: str,
    create_folder: bool = False,
) -> None:
    """Download the file from the URL and save it as folder_path/filename.

    If the downloads folder does not exist, it will be created due to the
    create_folder argument.

    Args:
        url (str): The URL of the file to be downloaded.
        folder_path (str | Path): The path where the file should be saved.
        file_name (str): The name to save the downloaded file.
        create_folder (bool): If True, creates the folder if it does not exist; otherwise, exit.

    Returns:
        None
    """
    folder = Path(folder_path)
    folder_file = folder / file_name

    # Check if the folder exists
    if not folder.exists():
        if create_folder:
            folder.mkdir(parents=True)
            print(f"The folder '{folder_path}' was created.")
        else:
            print(f"The folder '{folder_path}' does not exist. Exiting...")
            return

    # Check if the file already exists
    if folder_file.exists():
        print(f"The file '{file_name}' already exists in the folder '{folder_path}'.")
    else:
        # Download the URL to the file
        response = requests.get(url)
        folder_file.write_bytes(response.content)
        print(f"File '{file_name}' has been downloaded to '{folder_path}'.")


def barra2_point(barra2_var: list,
                 lat_lon_point: LatLonPoint,
                 start_datetime: str | datetime,
                 end_datetime: str | datetime,
                 fileout_prefix: str = None,
                 fileout_folder: str = 'cache',
                 fileout_type: str = 'csv_file') -> None:
    """Download barra2 data based on the url and variables list
    for each month between start and end datetime.

    Args:
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
        Implement grid netCDF download
        Set default fileout_prefix if not set by user
    """

    # base thredds url for BARRA2 11km 1hour reanalysis data
    barra2_aus11_url = ("https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5"
                            "/historical/hres/BARRA-R2/v1/1hr/{var}/latest/"
                            "{var}_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc")

    # assign to base_url for future functionality to include switching for multiple urls
    base_url = barra2_aus11_url

    # Set file extension based on fileout_type
    match fileout_type:
        case 'csv_file':
            fileout_ext = '.csv'
        # case 'netcdf_file':
        #     fileout_ext = '.nc'
        case _:
            raise ValueError(f"Unsupported fileout_type: {fileout_type}")

    # loop through each variable requested for download as each variable is saved in a separate url
    for var in barra2_var:
        # loop through each month as each BARRA2 file is saved by month todo check index enumerate addition works
        for date in list_months(start_datetime, end_datetime, freq="MS"):
            year = date.year
            month = date.month
            time_start = date
            time_start_str = date.isoformat() + 'Z'
            # Get the number of days in the current month
            days_in_month = calendar.monthrange(year, month)[1]
            time_end = date + timedelta(days=days_in_month) + timedelta(hours=-1)
            time_end_str = time_end.isoformat() + 'Z'

            # update thredds_base_url and set as url for request
            url = base_url.format(var=var, year=year, month=month)

            # add url parameters to base_url
            url += (f"?var={var}&latitude={lat_lon_point['lat']}&longitude={lat_lon_point['lon']}&time_start={time_start_str}&time_end={time_end_str}&accept"
                    f"={fileout_type}")
            fileout_name = f'{fileout_prefix}_{var}_{time_start.strftime('%Y%m%d')}_{time_end.strftime('%Y%m%d')}{fileout_ext}'
            folder_path = fileout_folder
            download_file(url, folder_path, fileout_name, create_folder=True)

            # todo add option to name file_prefix using BARRA2 node; might need index 0 check
            # if fileout_prefix is None:
            #   fileout_prefix = BARRA2_aus11_index[lat_lon_point['lat']][lat_lon_point['lon']]
