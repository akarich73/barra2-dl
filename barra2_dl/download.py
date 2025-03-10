"""This module contains the barra2 download function(s)."""
import calendar
import logging
import sys
import time
from datetime import datetime, timedelta
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from pathlib import Path

import pandas as pd
import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = [
    'point_data_urlfilenames',
    'download_file',
    'download_serial',
    'download_multithread',
]

type URLFilenamePair = tuple[str, str]


def _list_months(
    start_datetime: str,
    end_datetime: str,
    freq: str = 'MS',
) -> list:
    """Generate list of months from input start and end datetime for download url file loop.

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
    except ValueError as error:
        raise ValueError(f'Invalid start_datetime provided: {error}') from None

    try:
        pd.to_datetime(end_datetime)
    except ValueError as error:
        raise ValueError(f'Invalid end_datetime provided: {error}') from None

    return pd.date_range(start=start_datetime, end=end_datetime, freq=freq).tolist()


def _list_timestamp_range(
    dataframe: pd.DataFrame,
    timestamp_column: str,
) -> list:
    """Get a list containing the range between the first and last timestamp in the specified column of the DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the timestamp column.
        timestamp_column (str): The name of the timestamp column in the DataFrame.

    Returns:
        list: A list containing the first and last timestamp.

    Raises:
        ValueError: if timestamp_column does not exist.

    Todo:
        Not implemented function for only downloading new data based on existing time range.
        Add valid csv file check for downloading files from last 3 months
    """
    if timestamp_column not in dataframe.columns:
        raise ValueError(f'Column <{timestamp_column}> does not exist in the DataFrame.')

    # Ensure the column is of datetime type
    dataframe[timestamp_column] = pd.to_datetime(dataframe[timestamp_column])

    # Sort the DataFrame by the timestamp column
    dataframe = dataframe.sort_values(by=timestamp_column)

    # Get the first and last timestamp
    first_timestamp = dataframe[timestamp_column].iloc[0]
    last_timestamp = dataframe[timestamp_column].iloc[-1]

    return [first_timestamp, last_timestamp]


def point_data_urlfilenames(
    barra2_vars: list,
    latitude: float | int,
    longitude: float | int,
    start_datetime: str | datetime,
    end_datetime: str | datetime,
    fileout_prefix: str = None,
    fileout_type: str = 'csv_file',
) -> list[URLFilenamePair]:
    """Generate a list of URLs and Filenames for downloading barra2 point data.

    Uses nearest node for each var in barra2_vars for a given time period.
    List of URLs and filenames can be used to download files.
    URLs and filenames for each month between start and end datetime.
    filenames as f'{fileout_prefix}_{var}_{time_start[:10]}_{time_end[:10]}.{fileout_type}'
    Currently limited to csv file download only.

    Args:
        barra2_vars (list): Use from barra2-dl.globals or set explicitly
        latitude (float |int):  Point latitude.
        longitude (float |int):  Point longitude.
        start_datetime (str | datetime): Used to define start of inclusive download period
        end_datetime (str | datetime): Used to define end of inclusive download period
        fileout_prefix (str): Optional prefix for downloaded file. E.g. location reference
        fileout_type (str): Output file option, 'csv_file'

    Returns:
        point_data_urlfilenamepair(list[URLFilenamePair])

    Raises:
        ValueError: If not csv file set for export.

    Todo:
        Add additional output types
        Implement grid netCDF download
        Set default fileout_prefix if not set by user
        Add option to name file_prefix using BARRA2 node if fileout_prefix is None
    """
    # base thredds url for BARRA2 11km 1hour reanalysis data
    barra2_aus11_url = (
        'https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5'
        '/historical/hres/BARRA-R2/v1/1hr/{var}/latest/'
        '{var}_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc'
    )

    # assign to base_url for future functionality to include switching for multiple urls
    base_url = barra2_aus11_url

    # Set file extension based on fileout_type
    match fileout_type:
        case 'csv_file':
            fileout_ext = 'csv'
        case _:
            logger.error(f'Unsupported fileout_type: {fileout_type}')
            raise ValueError(f'{fileout_type} is currently not supported.')

    # create empty list for url and filename
    point_data_urlfilenamepair = []

    # loop through each variable requested for download as each variable is saved in a separate url
    for barra2_var in barra2_vars:
        # loop through each month as each BARRA2 file is saved by month todo check index enumerate addition works
        for date in _list_months(start_datetime, end_datetime, freq='MS'):
            year = date.year
            month = date.month
            time_start = date
            time_start_str = date.isoformat() + 'Z'
            # Get the number of days in the current month
            days_in_month = calendar.monthrange(year, month)[1]
            time_end = date + timedelta(days=days_in_month) + timedelta(hours=-1)
            time_end_str = time_end.isoformat() + 'Z'

            # update thredds_base_url and set as url for request
            url = base_url.format(var=barra2_var, year=year, month=month)

            # add url parameters to base_url
            url += (
                f"?var={barra2_var}&latitude={latitude}&longitude={longitude}"
                f'&time_start={time_start_str}&time_end={time_end_str}'
                f'&accept={fileout_type}'
            )

            # set fileout_name
            fileout_name = (
                f'{fileout_prefix}_'
                f'{barra2_var}_'
                f"{time_start.strftime('%Y%m%d')}_{time_end.strftime('%Y%m%d')}"
                f'.{fileout_ext}'
            )
            # append url and filename as tuple
            point_data_urlfilenamepair.append((url, fileout_name))

    return point_data_urlfilenamepair


def get_point_data(
    barra2_vars: list,
    latitude: float | int,
    longitude: float | int,
    start_datetime: str | datetime,
    end_datetime: str | datetime,
    fileout_prefix: str = None,
    fileout_folder: str | Path = 'cache',
    fileout_type: str = 'csv_file',
) -> None:
    """Download barra2 point data as individual files for each var in barra2_vars.

    Data downloaded for each month between start and end datetime.
    Downloaded files into fileout_folder as f'{fileout_prefix}_{var}_{time_start[:10]}_{time_end[:10]}.csv'
    Currently limited to csv file download only.

    Args:
        barra2_vars (list): Use from barra2-dl.globals or set explicitly
        latitude (float |int):  Point latitude.
        longitude (float |int):  Point longitude.
        start_datetime (str | datetime): Used to define start of inclusive download period
        end_datetime (str | datetime): Used to define end of inclusive download period
        fileout_prefix (str): Optional prefix for downloaded file. E.g. location reference
        fileout_folder (str | Path): Relative or absolute path for downloaded files
        fileout_type (str): Output file option, 'csv_file'

    Returns: None

    Raises:
        ValueError: If not csv file set for export.

    Todo:
        Add set list of output format options
        Add additional output types
        Implement grid netCDF download
        Set default fileout_prefix if not set by user
        Add option to name file_prefix using BARRA2 node if fileout_prefix is None
    """
    # base thredds url for BARRA2 11km 1hour reanalysis data
    barra2_aus11_url = (
        'https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5'
        '/historical/hres/BARRA-R2/v1/1hr/{var}/latest/'
        '{var}_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc'
    )

    # assign to base_url for future functionality to include switching for multiple urls
    base_url = barra2_aus11_url

    # Set file extension based on fileout_type
    match fileout_type:
        case 'csv_file':
            fileout_ext = 'csv'
        case _:
            logger.error(f'Unsupported fileout_type: {fileout_type}')
            raise ValueError(f'{fileout_type} is currently not supported.')

    # loop through each variable requested for download as each variable is saved in a separate url
    for barra2_var in barra2_vars:
        # loop through each month as each BARRA2 file is saved by month todo check index enumerate addition works
        for date in _list_months(start_datetime, end_datetime, freq='MS'):
            year = date.year
            month = date.month
            time_start = date
            time_start_str = date.isoformat() + 'Z'
            # Get the number of days in the current month
            days_in_month = calendar.monthrange(year, month)[1]
            time_end = date + timedelta(days=days_in_month) + timedelta(hours=-1)
            time_end_str = time_end.isoformat() + 'Z'

            # update thredds_base_url and set as url for request
            url = base_url.format(var=barra2_var, year=year, month=month)

            # add url parameters to base_url
            url += (
                f"?var={barra2_var}&latitude={latitude}&longitude={longitude}"
                f'&time_start={time_start_str}&time_end={time_end_str}'
                f'&accept={fileout_type}'
            )

            # set fileout_name
            fileout_name = (
                f'{fileout_prefix}_'
                f'{barra2_var}_'
                f"{time_start.strftime('%Y%m%d')}_{time_end.strftime('%Y%m%d')}"
                f'.{fileout_ext}'
            )

            # download file
            download_file(url, fileout_folder, fileout_name)


def download_file(
    url: str,
    file_name: str,
    folder_path: str | Path,
) -> None:
    """Download the file from the url and save it as folder_path/filename.

    If the downloads folder does not exist, it will be created due to the
    create_folder argument.

    Args:
        url (str): The URL of the file to be downloaded.
        file_name (str): The name to save the downloaded file.
        folder_path (str | Path): The path where the file should be saved.

    Returns: None

    Raises:
        FileNotFoundError: If folder does not exist.
    """
    folder = Path(folder_path)
    folder_file = folder / file_name

    # Check if the folder exists
    if not folder.exists():
        logger.error(f'{folder_path} does not exist.')
        raise FileNotFoundError(f'The folder {folder_path} does not exist. Create folder first.')

    # Check if the file already exists else download the url to the file
    if folder_file.exists():
        logger.info(f'<{file_name}> already exists in the <{folder_path}>. File not downloaded.')
        sys.stdout.write(f'<{file_name}> already exists in the folder <{folder_path}>. File not downloaded.')
        sys.stdout.write('\n')
    else:
        response = requests.get(url) #, timeout=20
        # check file is not empty or contains server error 'FileNotFound: No such file or directory'
        # Check if the request was successful
        if response.status_code == 200:
            # write content to folder_file
            folder_file.write_bytes(response.content)
            logger.info(f'<{file_name}> downloaded to <{folder_path}>')
            sys.stdout.write(f'<{file_name}> downloaded to <{folder_path}>')
            sys.stdout.write('\n')
        else:
            logger.info(f'<{file_name}> Failed to download. Status code: {response.status_code}')
            sys.stdout.write(f'<{file_name}> Failed to download. Status code: {response.status_code}')
            sys.stdout.write('\n')


def download_serial(
    urlfilenames: list[URLFilenamePair],
    folder_path: str | Path,
) -> None:
    """Download all files from urls in list of URLFilenamePairs and save it as folder_path/filename, using a loop.

    Args:
        urlfilenames (list[URLFilenamePair]): A list of URLFilenamePair of the files to be downloaded.
        folder_path (str | Path): The path where the file should be saved.

    Returns: None

    Raises: None

    References:
        https://opensourceoptions.com/use-python-to-download-multiple-files-or-urls-in-parallel/
        https://medium.com/towards-data-science/use-python-to-download-multiple-files-or-urls-in-parallel-1759da9d6535
    """
    # download multiple files in loop
    t0 = time.time()
    for url, filename in urlfilenames:
        download_file(url,filename,folder_path)
    logger.info(f'Download time <{time.time() - t0}>')
    sys.stdout.write(f'Download time: <{time.time() - t0}>')
    sys.stdout.write('\n')


def download_multithread(
    urlfilenames: list[URLFilenamePair],
    folder_path: str | Path,
) -> None:
    """Download all files from urls in list of URLFilenamePairs and save it as folder_path/filename, using multithread.

    Args:
        urlfilenames (list[URLFilenamePair]): A list of URLFilenamePair of the files to be downloaded.
        folder_path (str | Path): The path where the file should be saved.

    Returns: None

    Raises: None

    References:
        https://opensourceoptions.com/use-python-to-download-multiple-files-or-urls-in-parallel/
        https://medium.com/towards-data-science/use-python-to-download-multiple-files-or-urls-in-parallel-1759da9d6535
    """
    # download multiple files in parallel
    cpus = cpu_count()
    t0 = time.time()
    with ThreadPool(cpus - 1) as pool:
        pool.starmap(download_file, [(url, filename, folder_path) for url, filename in urlfilenames])
    logger.info(f'Download time <{time.time() - t0}>')
    sys.stdout.write(f'Download time: <{time.time() - t0}>')
    sys.stdout.write('\n')
