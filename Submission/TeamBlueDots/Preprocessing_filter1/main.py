import pandas as pd
from geopy.distance import great_circle
import datetime
from itertools import combinations
from Submission.functions import haversine, filter_df, box_intervals, time_overlap

df_file = '../Data/AIS_2017_12_Zone11.csv'

# Rebuilds the dataframe from the chunks
df = pd.read_csv(df_file)
print('File read.', df.shape)

df = filter_df(df)

date_min = df.Date.min()  # start date
date_max = df.Date.max()  # end date

delta = date_max - date_min         # timedelta

dates = []
for i in range(delta.days + 1):
    dates.append(date_min + datetime.timedelta(i))

for date in dates:
    date_start_time = datetime.datetime.now()
    print(date)
    df_date = df[(df.Date >= date) & (df.Date < date+datetime.timedelta(1))]

    intervals = box_intervals(df_date)

    num_boxes = len(intervals['lat']*len(intervals['lon']))
    print('Number of boxes:', num_boxes)
    boxes_checked = 0

    ship_combos_checked = set()
    ships_interactions = 0
    # Loop through each sub-box
    for lat_i, temp_box_lat in enumerate(intervals['lat']):
        for lon_i, temp_box_lon in enumerate(intervals['lon']):
            boxes_checked = boxes_checked + 1
            if boxes_checked % 1000 == 0:
                print('Boxes checked:', boxes_checked)
                print('Total ships comparisons for this day:', len(ship_combos_checked))
                print('Total ship interactions for this day:', ships_interactions)
            # Don't loop through end of box
            if (lat_i < len(intervals['lat']) - 3) & (lon_i < len(intervals['lon']) - 3):
                # print('Starting box', temp_box_lat, temp_box_lon)
                interactions = pd.DataFrame
                # Get all data within box
                df_box = df_date[(df_date.LAT >= temp_box_lat)&(df_date.LAT <= intervals['lat'][lat_i+2])&(df_date.LON >= temp_box_lon)&(df_date.LON <= intervals['lon'][lon_i+2])]
                # Get ids of all ships that existed in the box
                ships = list(set(df_box.MMSI.tolist()))
                # If more than 1 ship
                if ships is not None and len(ships) > 1:
                    ships.sort()
                    # Create all combinations of ships that haven't been checked yet
                    ship_combinations = set(list(combinations(ships, 2)))  # 2 for pairs, 3 for triplets, etc
                    ship_combinations = ship_combinations - ship_combos_checked
                    for combo in ship_combinations:
                        # Check for time overlap
                        if time_overlap((df_box.BaseDateTime[df_box.MMSI == combo[0]].min(), df_box.BaseDateTime[df_box.MMSI == combo[0]].max()), (df_box.BaseDateTime[df_box.MMSI == combo[1]].min(), df_box.BaseDateTime[df_box.MMSI == combo[1]].max())):
                            # Check distance between ships
                            ship_combos_checked.add(combo)
                            distance = great_circle((df_box.LAT[df_box.MMSI == combo[0]].iloc[0], df_box.LON[df_box.MMSI == combo[0]].iloc[0]), (df_box.LAT[df_box.MMSI == combo[1]].iloc[0], df_box.LON[df_box.MMSI == combo[1]].iloc[0])).feet / 3
                            if distance <= 8000:
                                ships_interactions = ships_interactions + 1
    date_end_time = datetime.datetime.now()
    time_delta = date_end_time - date_start_time
    print('Time to process:', time_delta.seconds / 60, 'minutes')
