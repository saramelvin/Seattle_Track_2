import pandas as pd
import numpy as np
from geopy.distance import great_circle


def max_min_lat_lon(df):
    data = {
        'lat_max': df['LAT'].max(),
        'lat_min': df['LAT'].min(),
        'lon_max': df['LON'].max(),
        'lon_min': df['LON'].min()
    }
    return data


df11 = pd.read_csv('data/AIS_2017_12_Zone11.csv')

borders = max_min_lat_lon(df11)
print(borders)
border_min_gps = (borders['lat_min'], borders['lon_min'])
border_max_lat = (borders['lat_max'], borders['lon_min'])
border_max_lon = (borders['lat_min'], borders['lon_max'])

lat_distance = great_circle(border_min_gps, border_max_lat).feet / 3
lon_distance = great_circle(border_min_gps, border_max_lon).feet / 3

lat_distance_num_intervals = lon_distance / 4000
lon_distance_num_intervals = lat_distance / 4000

lat_distance_intervals = np.linspace(borders['lat_min'], borders['lat_max'], lat_distance_num_intervals)
lon_distance_intervals = np.linspace(borders['lon_min'], borders['lon_max'], lon_distance_num_intervals)

print(lat_distance_intervals, len(lat_distance_intervals))
print(lon_distance_intervals, len(lon_distance_intervals))

for lat in lat_distance_intervals:
    for lon in lon_distance_intervals:


df_sectors = df11[()&()&()&()]
temp_df =     df2[(df2.BaseDateTime > time_min)&(df2.BaseDateTime < time_max)]

