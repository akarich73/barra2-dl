"""
This module contains global or default variables required to download barra2-dl data from thredds.nci.org.au.
"""
from typing import TypedDict

# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------

class LatLonPoint(TypedDict):
    """TypedDict to store a point as latitude and longitude.

    Attributes:
        lat (float): latitude.
        lon (float): longitude.

    """
    lat: float
    lon: float


class LatLonBBox(TypedDict):
    """TypedDict to store a north south east west bounding box by latitude and longitude.

        Attributes:
            north (float): latitude.
            south (float): latitude.
            east (float): longitude.
            west (float): longitude.

        Todo:
        Add checks to make sure co-ordinates are correct with respect to each other.
        """
    north: float
    south: float
    east: float
    west: float

# -----------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------

# barra2_aus11_extents
barra2_aus11_lat_lon_bbox = LatLonBBox(north=-23.0, west=133.0, east=134.0, south=-24)

# base thredds url for BARRA2 11km 1hour reanalysis data
barra2_aus11_csv_url = ("https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5"
                        "/historical/hres/BARRA-R2/v1/1hr/{var}/latest/"
                        "{var}_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc")

# index for barra2 used to join separate files
barra2_index = ['time', 'station', 'latitude[unit="degrees_north"]', 'longitude[unit="degrees_east"]']

# set list of BARRA2 variables to download default list is eastward wind (ua*), northward wind (va*), and air temperature at 50m (ta50m)
barra2_var_wind_all = ["ua50m", "va50m", "ua100m", "va100m", "ua150m", "va150m", "ta50m"]

# optional limited variables to test
barra2_var_wind_50m = ["ua50m", "va50m", "ta50m"]

# output file format todo add list of output format options
point_output_format = "csv_file"
# grid_output_format = "netcdf3"
