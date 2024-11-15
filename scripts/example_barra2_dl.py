#%% md
# # barra2-dl point data demo
# This script uses barra2-dl to download BARRA2 AUS11 files for a list of variables. Individual data files will be
# saved as csv files in a cache folder, then merged into a single pandas dataframe. As a final step the wind ua and va
# components are converted to v and phi_met, before saving to a new csv file in an output folder.
#
# The first step is to import the necessary python packages and modules from barra2_dl. Also from barra2_dl.globals we
# import some pre-configured default variables to download.
#%%
from datetime import datetime
from pathlib import Path

import barra2_dl
from barra2_dl.globals import (
    BARRA2_AUS11_INDEX,
    barra2_var_wind_50m,
    barra2_var_wind_default,
)

#%%
print('BARRA2_AUS11_INDEX: ' + BARRA2_AUS11_INDEX.__str__())
print('barra2_var_wind_50m: ' + barra2_var_wind_50m.__str__())
print('barra2_var_wind_default: ' + barra2_var_wind_default.__str__())
#%% md
# ## Set variables
# Set the cache and output folders.
#%%
cache_dir = r'scripts\cache'
output_dir = r'scripts\output'
#%% md
# Set the location point for downloading. This can either be set explicitly as a Dictionary, or using the
# pre-configured LatLonPoint class in barra2_dl.mapping module. Point data is downloaded to the nearest node.
#%%
# centre of Australia used for demo
lat_lon_point = dict(lat=-23.5527472, lon=133.3961111)

# or use custom class
from barra2_dl.mapping import LatLonPoint

lat_lon_point = LatLonPoint(-23.5527472, 133.3961111)

print(lat_lon_point)
#%% md
# Set start and end time for download.
#%%
start_datetime = datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
end_datetime = datetime.strptime("2023-03-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
#%% md
# Set output file custom name prefix to indicate a device or project location for the downloaded data. I.e.
# use project or location name.
#
#%%
fileout_prefix = "demo"
#%% md
# ## Download point data
# Use get_point_data to download closest node for the desired variables into the target cache folder.
#%%
barra2_dl.download.get_point_data(
    barra2_vars = barra2_var_wind_default,
    latitude = lat_lon_point.lat,
    longitude = lat_lon_point.lon,
    start_datetime= start_datetime,
    end_datetime = end_datetime,
    fileout_prefix = fileout_prefix,
    fileout_folder= cache_dir,
)
#%% md
# ## Combine data
# Merge downloaded csvs into a new dataframe. Optionally export merged data to a new csv.
#%%
df_merged = barra2_dl.merge.merge_csvs_to_df(
    filein_folder= cache_dir,
    filename_pattern=f'{fileout_prefix}*.csv',
    index_for_join=BARRA2_AUS11_INDEX,
)
print(df_merged.head())
#%%
df_merged.to_csv(Path(output_dir) / f"{fileout_prefix}_merged_{start_datetime.strftime("%Y%m%d")}_{end_datetime.strftime("%Y%m%d")}.csv", index=False)
#%% md
# ## Convert wind speed components
# Using the merged dataframe, convert ua and va to v and phi_met, and export to new csv file
#%%
df_converted = barra2_dl.convert.convert_wind_components(df_merged)
print(df_converted.head())
#%%
df_converted.to_csv(Path(output_dir) / f"{fileout_prefix}_converted_{start_datetime.strftime("%Y%m%d")}_{end_datetime.strftime("%Y%m%d")}.csv", index=False)
#%% md
# The merged and converted data is now ready to import into your favourite wind analysis program...
