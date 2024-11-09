"""This module contains global or default variables required to download barra2-dl data from thredds.nci.org.au."""

# index for barra2 used to join separate files
BARRA2_AUS11_INDEX = [
    'time',
    'station',
    'latitude[unit="degrees_north"]',
    'longitude[unit="degrees_east"]',
]

# BARRA2 wind speed variable pairs
BARRA2_AUS11_WIND_VARS = [
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

# set list of BARRA2 variables to download default list is eastward wind (ua*), northward wind (va*), and air temperature at 50m (ta50m)
barra2_var_wind_custom = ['ua50m', 'va50m', 'ua100m', 'va100m', 'ua150m', 'va150m', 'ta50m']

# optional limited variables to test
barra2_var_wind_50m = ['ua50m', 'va50m', 'ta50m']
