from datetime import datetime

import pytest
import os
from pandas import Timestamp

import barra2_dl.download, barra2_dl.globals
from barra2_dl.mapping import LatLonPoint
from barra2_dl.globals import (
    BARRA2_AUS11_INDEX,
    barra2_var_wind_50m,
    barra2_var_wind_default,
)

@pytest.mark.parametrize(('start_datetime', 'end_datetime', 'expected'), [
                            ('1/1/2023','1/1/2024',
                            [Timestamp('2023-01-01 00:00:00'),
                            Timestamp('2023-02-01 00:00:00'),
                            Timestamp('2023-03-01 00:00:00'),
                            Timestamp('2023-04-01 00:00:00'),
                            Timestamp('2023-05-01 00:00:00'),
                            Timestamp('2023-06-01 00:00:00'),
                            Timestamp('2023-07-01 00:00:00'),
                            Timestamp('2023-08-01 00:00:00'),
                            Timestamp('2023-09-01 00:00:00'),
                            Timestamp('2023-10-01 00:00:00'),
                            Timestamp('2023-11-01 00:00:00'),
                            Timestamp('2023-12-01 00:00:00'),
                            Timestamp('2024-01-01 00:00:00')]
                           ),
])
def test_list_months(start_datetime: str, end_datetime: str, expected: list) -> None:
    """Test with parametrization."""
    assert barra2_dl.download._list_months(start_datetime, end_datetime) == expected

@pytest.mark.parametrize((
    'barra2_vars',
    'latitude',
    'longitude',
    'start_datetime',
    'end_datetime',
    'fileout_prefix',
    'expected'), [
    (barra2_var_wind_default,
    LatLonPoint(-23.5527472, 133.3961111).lat,
    LatLonPoint(-23.5527472, 133.3961111).lon,
    datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
    datetime.strptime("2023-03-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
     'demo',
    [('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua50m/latest/ua50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=ua50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
    'demo_ua50m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua50m/latest/ua50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=ua50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_ua50m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua50m/latest/ua50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=ua50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_ua50m_20230301_20230331.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va50m/latest/va50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=va50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
      'demo_va50m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va50m/latest/va50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=va50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_va50m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va50m/latest/va50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=va50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_va50m_20230301_20230331.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua100m/latest/ua100m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=ua100m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
      'demo_ua100m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua100m/latest/ua100m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=ua100m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_ua100m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua100m/latest/ua100m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=ua100m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_ua100m_20230301_20230331.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va100m/latest/va100m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=va100m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
      'demo_va100m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va100m/latest/va100m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=va100m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_va100m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va100m/latest/va100m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=va100m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_va100m_20230301_20230331.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua150m/latest/ua150m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=ua150m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
      'demo_ua150m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua150m/latest/ua150m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=ua150m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_ua150m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ua150m/latest/ua150m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=ua150m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_ua150m_20230301_20230331.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va150m/latest/va150m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=va150m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
      'demo_va150m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va150m/latest/va150m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=va150m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_va150m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/va150m/latest/va150m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=va150m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_va150m_20230301_20230331.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ta50m/latest/ta50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202301-202301.nc?var=ta50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-01-01T00:00:00Z&time_end=2023-01-31T23:00:00Z&accept=csv_file',
      'demo_ta50m_20230101_20230131.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ta50m/latest/ta50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202302-202302.nc?var=ta50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-02-01T00:00:00Z&time_end=2023-02-28T23:00:00Z&accept=csv_file',
      'demo_ta50m_20230201_20230228.csv'),
     ('https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/historical/hres/BARRA-R2/v1/1hr/ta50m/latest/ta50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_202303-202303.nc?var=ta50m&latitude=-23.5527472&longitude=133.3961111&time_start=2023-03-01T00:00:00Z&time_end=2023-03-31T23:00:00Z&accept=csv_file',
      'demo_ta50m_20230301_20230331.csv')]
     ),
])
def test_get_point_data_urls(
    barra2_vars,
    latitude,
    longitude,
    start_datetime,
    end_datetime,
    fileout_prefix,
    expected) -> None:
    """Test with parametrization."""
    assert barra2_dl.download.get_point_data_urlfilenames(
        barra2_vars,
        latitude,
        longitude,
        start_datetime,
        end_datetime,
        fileout_prefix,
    ) == expected

# todo fix this to test downloads
@pytest.mark.parametrize((
    'barra2_vars',
    'latitude',
    'longitude',
    'start_datetime',
    'end_datetime',
    'fileout_prefix',),[
    (barra2_var_wind_default,
    LatLonPoint(-23.5527472, 133.3961111).lat,
    LatLonPoint(-23.5527472, 133.3961111).lon,
    datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
    datetime.strptime("2023-03-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
     'demo')])
def test_download_files(
    barra2_vars,
    latitude,
    longitude,
    start_datetime,
    end_datetime,
    fileout_prefix,
    tmp_path) -> None:
    download_folder = tmp_path / 'cache'
    download_folder.mkdir()

    """Test with parametrization."""
    urlfilenames = barra2_dl.download.get_point_data_urlfilenames(
        barra2_vars,
        latitude,
        longitude,
        start_datetime,
        end_datetime,
        fileout_prefix,
    )
    barra2_dl.download._download_files_multithread(urlfilenames, download_folder)

    for item in [item[1] for item in urlfilenames]:
        filename = download_folder / os.path.basename(item)
        assert filename.exists()





