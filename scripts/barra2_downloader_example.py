"""
Example for using barra2-dl to download files
"""

import barra2_dl
from datetime import datetime
from barra2_dl.globals import barra2_aus11_csv_url, barra2_var_wind_all, barra2_var_wind_50m, barra2_index

# relative directory for caching downloaded files
cache_dir = r'scripts\cache'
output_dir = r'scripts\output'

# -----------------------------------------------------------------------------
# CUSTOMS
# -----------------------------------------------------------------------------

# set location todo implement grid netCDF download
lat_lon_point = dict(lat=-23.5527472, lon=133.3961111)

# set time ref https://stackoverflow.com/questions/17594298/date-time-formats-in-python
start_datetime = datetime.strptime("2023-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
end_datetime = datetime.strptime("2023-03-31T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

# set output file custom name prefix to indicate a device or project location for the downloaded data
output_filename_prefix = "test"


# -----------------------------------------------------------------------------
# RUNTIME PROCEDURE
# -----------------------------------------------------------------------------
def main():
    """runtime for tryBARRA2"""
    barra2_dl.downloaders.barra2_point_downloader(barra2_aus11_csv_url,
                                                  barra2_var_wind_50m,
                                                  lat_lon_point,
                                                  start_datetime,
                                                  end_datetime,
                                                  fileout_prefix = 'demo',
                                                  fileout_folder=r'scripts\cache',
                                                  )

    # todo moved from original runtime
    # export combined to csv
    # df_combined.to_csv(
    #     os.path.join(output_dir,
    #                  f"{output_filename_prefix}_combined_{start_date_time.strftime("%Y%m%d")}_{end_date_time.strftime("%Y%m%d")}.csv"))


if __name__ == '__main__':
    main()
