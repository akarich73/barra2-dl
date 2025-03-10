"""This module contains global or default variables required to download barra2-dl data from thredds.nci.org.au."""

# Todo from .mapping import LatLonBBox

# index for barra2 used to join separate files
BARRA2_INDEX = [
    'time',
    'station',
    'latitude[unit="degrees_north"]',
    'longitude[unit="degrees_east"]',
]

# BARRA2 wind speed variable pairs
BARRA2_WIND_VARS = [
    ('ua10m', 'va10m', '10m[unit="m s-1"]'),
    ('ua20m', 'va20m', '20m[unit="m s-1"]'),
    ('ua30m', 'va30m', '30m[unit="m s-1"]'),
    ('ua50m', 'va50m', '50m[unit="m s-1"]'),
    ('ua70m', 'va70m', '70m[unit="m s-1"]'),
    ('ua100m', 'va100m', '100m[unit="m s-1"]'),
    ('ua150m', 'va150m', '150m[unit="m s-1"]'),
    ('ua200m', 'va200m', '200m[unit="m s-1"]'),
    ('ua250m', 'va250m', '250m[unit="m s-1"]'),
    ('ua300m', 'va300m', '30m[unit="m s-1"]'),
    ('ua400m', 'va400m', '400m[unit="m s-1"]'),
    ('ua500m', 'va500m', '500m[unit="m s-1"]'),
    ('ua600m', 'va600m', '600m[unit="m s-1"]'),
    ('ua700m', 'va700m', '700m[unit="m s-1"]'),
    ('ua850m', 'va850m', '850m[unit="m s-1"]'),
    ('ua925m', 'va925m', '925m[unit="m s-1"]'),
    ('ua1000m', 'va1000m', '1000m[unit="m s-1"]'),
]

# barra2_aus11_extents http://www.bom.gov.au/research/publications/researchreports/BRR-067.pdf
# Todo BARRA2_AU11_LATLONBBOX = LatLonBBox(north=12.95, south=-57.97, east=207.39, west=88.48)

# Todo BARRA2_AUS11_GRID_SPACING = 0.11

# default list of BARRA2 variables for wind analysis
BARRA2_VAR_WIND_DEFAULT = ['ua50m', 'va50m', 'ua100m', 'va100m', 'ua150m', 'va150m', 'ta50m']

# optional limited variables to test
BARRA2_VAR_WIND_50 = ['ua50m', 'va50m', 'ta50m']

# Base BOM BARRA2 thredds urls for NetCDF Subset Service for Grids As Points
# Reference url:
# https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5/
# historical/hres/BARRA-R2/v1/1hr/va50m/latest/va50m_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_197901-197901.nc?
# var=va50m&latitude=-23.5527472&longitude=133.3961111
# &time_start=1979-01-01T00:00:00Z&time_end=1979-01-31T23:00:00Z&&&accept=csv
BARRA2_URL_AUS11_1HR = (
    'https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUS-11/BOM/ERA5'
    '/historical/hres/BARRA-R2/v1/1hr/{var}/latest/'
    '{var}_AUS-11_ERA5_historical_hres_BOM_BARRA-R2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc'
    '?var={var}&latitude={latitude}&longitude={longitude}'
    '&time_start={time_start_str}&time_end={time_end_str}'
    '&timeStride=&vertCoord='
    '&accept={fileout_type}'
)

# Reference url:
# https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUST-04/BOM/ERA5/
# historical/hres/BARRA-C2/v1/1hr/va50m/latest/va50m_AUST-04_ERA5_historical_hres_BOM_BARRA-C2_v1_1hr_197901-197901.nc?
# var=va50m&latitude=-23.5527472&longitude=133.3961111
# &time_start=1979-01-01T00:00:00Z&time_end=1979-01-31T23:00:00Z&&&accept=csv
BARRA2_URL_AUST04_1HR = (
    'https://thredds.nci.org.au/thredds/ncss/grid/ob53/output/reanalysis/AUST-04/BOM/ERA5/'
    'historical/hres/BARRA-C2/v1/1hr/{var}/latest/'
    '{var}_AUST-04_ERA5_historical_hres_BOM_BARRA-C2_v1_1hr_{year}{month:02d}-{year}{month:02d}.nc'
    '?var={var}&latitude={latitude}&longitude={longitude}'
    '&time_start={time_start_str}&time_end={time_end_str}'
    '&timeStride=&vertCoord='
    '&accept={fileout_type}'
)
