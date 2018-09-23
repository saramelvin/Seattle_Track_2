import pandas as pd
import numpy as np
from geopy.distance import great_circle
import datetime


def max_min_lat_lon(df):
    data = {
        'lat_max': df['LAT'].max(),
        'lat_min': df['LAT'].min(),
        'lon_max': df['LON'].max(),
        'lon_min': df['LON'].min()
    }
    return data


df11 = pd.read_csv('data/AIS_2017_12_Zone11.csv')
print('File read.')

df11 = df11.sort_values(by='BaseDateTime', ascending=True)
print('Data sorted by time.')
df11.BaseDateTime = pd.to_datetime(df11.BaseDateTime, errors='raise')
df11['Date'] = df11.BaseDateTime.apply(lambda x: x.date())
print('Date/Time values converted to Date/Time objects.')

date_min = df11.Date.min()  # start date
date_max = df11.Date.max()  # end date

delta = date_max - date_min         # timedelta

dates=[]
for i in range(delta.days + 1):
    dates.append(date_min + datetime.timedelta(i))

for date in dates:
    print(date)
    df11_date = df11[(df11.Date >= date) & (df11.Date < date+datetime.timedelta(1))]
    print(df11_date.Date.max(), df11_date.Date.min())

    borders = max_min_lat_lon(df11_date)
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




i=0
for temp_box_lat in lat_distance_intervals:
    for temp_box_lon in lon_distance_intervals:
        i=i+1

# df11[(df11.MMSI == 357147000)|(df11.MMSI == 366760710)]
# df_sectors = df11[()&()&()&()]
# temp_df =     df2[(df2.BaseDateTime > time_min)&(df2.BaseDateTime < time_max)]
# ships = df11.MMSI.tolist()
# if len(ships) > 1
#     for ship in ships:

