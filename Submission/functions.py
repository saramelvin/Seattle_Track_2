import pandas as pd
from numpy import radians as rad
from numpy import sin, cos, sqrt, arcsin
import numpy as np
from geopy.distance import great_circle


def filter_df(df):
    tug_tows = [21, 22, 31, 32, 52, 1023, 1025]
    df = df[~df.VesselType.isin(tug_tows)]
    print('Filtered out tugs.', df.shape)

    df = df[df.Status != 'moored']
    print('Filtered out moored.', df.shape)

    df = df.sort_values(by='BaseDateTime', ascending=True)
    print('Data sorted by time.')

    df.BaseDateTime = pd.to_datetime(df.BaseDateTime, errors='raise')
    df['Date'] = df.BaseDateTime.apply(lambda x: x.date())
    print('Date/Time values converted to Date/Time objects.')

    return df


def box_intervals(df):
    lat_max = df['LAT'].max()
    lat_min = df['LAT'].min()
    lon_max = df['LON'].max()
    lon_min = df['LON'].min()

    border_min_gps = (lat_min, lon_min)
    border_max_lat = (lat_max, lon_min)
    border_max_lon = (lat_min, lon_max)

    feet_to_yards = 3

    lat_distance = great_circle(border_min_gps, border_max_lat).feet / feet_to_yards
    lon_distance = great_circle(border_min_gps, border_max_lon).feet / feet_to_yards

    box_half_size_yards = 4000

    lat_distance_num_intervals = lon_distance / box_half_size_yards
    lon_distance_num_intervals = lat_distance / box_half_size_yards

    intervals = {
        'lat': list(np.linspace(lat_min, lat_max, lat_distance_num_intervals)),
        'lon': list(np.linspace(lon_min, lon_max, lon_distance_num_intervals))
    }

    # print(intervals['lat'], len(intervals['lat']))
    # print(intervals['lon'], len(intervals['lon']))

    return intervals


def haversine(coord1, coord2):
    dLat = rad(coord2[0] - coord1[0])
    dLon = rad(coord2[1]-coord1[1])
    lat1 = rad(coord1[0])
    lat2 = rad(coord2[0])
    a = sin(dLat/2)**2+cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c=2*arcsin(sqrt(a))
    R = 6372.8
    return R*c
