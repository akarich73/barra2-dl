"""
Example for using barra2-dl to download files
"""

from datetime import datetime
from pathlib import Path

import barra2_dl
from barra2_dl.globals import barra2_aus11_csv_url, barra2_aus11_wind_all, barra2_var_wind_50m, barra2_aus11_index

# set directory for caching downloaded files
cache_dir = r'cache'
output_dir = r'\output'

# set location
lat_lon_point = dict(lat=-23.5527472, lon=133.3961111)

# set time ref https://stackoverflow.com/questions/17594298/date-time-formats-in-python
start_datetime = datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
end_datetime = datetime.strptime("2023-03-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

# Option to set output file custom name prefix to indicate a device or project location for the downloaded data
output_filename_prefix = "demo"


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
def main():
    # download from barra2_aus11
    barra2_dl.downloader.barra2_point_downloader(barra2_aus11_csv_url,
                                                  barra2_var_wind_50m,
                                                  lat_lon_point,
                                                  start_datetime,
                                                  end_datetime,
                                                  fileout_prefix = 'demo',
                                                  fileout_folder=r'scripts\cache',
                                                  )

    # merge downloaded csvs into a new dataframe
    df_merged = barra2_dl.merger.merge_csvs_to_df(r"C:\Users\Richard.Gledhill\Local\PycharmProjects\barra2-dl\scripts\cache",index_for_join=barra2_aus11_index)
    # output to a new csv file
    df_merged.to_csv(
        Path(output_dir) / f"{output_filename_prefix}_merged_{start_datetime.strftime("%Y%m%d")}_{end_datetime.strftime("%Y%m%d")}.csv",
        index=False)

    # convert ua and va to v and phi
    df_converted = barra2_dl.merger.convert_wind_components(df_merged)
    # output to a new csv file
    df_converted.to_csv(
        Path(output_dir) / f"{output_filename_prefix}_converted_{start_datetime.strftime("%Y%m%d")}_{end_datetime.strftime("%Y%m%d")}.csv",
        index=False)

    # todo export combined to csv
    # df_combined.to_csv(
    #     os.path.join(output_dir,
    #                  f"{output_filename_prefix}_combined_{start_date_time.strftime("%Y%m%d")}_{end_date_time.strftime("%Y%m%d")}.csv"))


if __name__ == '__main__':
    main()
