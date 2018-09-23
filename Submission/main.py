import pandas as pd
from geopy.distance import great_circle
import datetime
from itertools import combinations
from Submission.functions import haversine, filter_df, box_intervals

df_file = 'data/AIS_2017_12_Zone11.csv'

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
    print(date)
    df_date = df[(df.Date >= date) & (df.Date < date+datetime.timedelta(1))]

    intervals = box_intervals(df_date)

    num_boxes = len(intervals['lat']*len(intervals['lon']))
    print('Number of boxes:', num_boxes)
    boxes_checked = 0

    ship_combos_checked = set()
    # Loop through each sub-box
    for lat_i, temp_box_lat in enumerate(intervals['lat']):
        for lon_i, temp_box_lon in enumerate(intervals['lon']):
            boxes_checked = boxes_checked + 1
            if boxes_checked % 1000 == 0:
                print('Boxes checked:', boxes_checked)
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
                    # print('Starting box', temp_box_lat, temp_box_lon)
                    # print('Count ships:', len(ships))
                    # Create all combinations of ships that haven't been checked yet
                    ship_combinations = set(list(combinations(ships, 2)))  # 2 for pairs, 3 for triplets, etc
                    ship_combinations = ship_combinations - ship_combos_checked
                    for combo in ship_combinations:
                        # check time in here
                        # Check distance between ships
                        ship_combos_checked.add(combo)
                        distance = great_circle((df_box.LAT[df_box.MMSI == combo[0]].iloc[0], df_box.LON[df_box.MMSI == combo[0]].iloc[0]), (df_box.LAT[df_box.MMSI == combo[1]].iloc[0], df_box.LON[df_box.MMSI == combo[1]].iloc[0])).feet / 3
                        if distance < 8000:
                            print(combo[0], combo[1])
                            # interactions.append(df_box[df_box.MMSI == combo[0]])
                            # interactions.append(df_box[df_box.MMSI == combo[1]])
                # print(interactions.shape)





# Range = namedtuple('Range', ['start', 'end'])
# r1 = Range(start=datetime.datetime(2012, 1, 15), end=datetime.datetime(2012, 5, 10))
# r2 = Range(start=datetime.datetime(2012, 3, 20), end=datetime.datetime(2012, 9, 15))
# def time_overlap(r1, r2):
#     latest_start = max(r1.start, r2.start)
#     earliest_end = min(r1.end, r2.end)
#     time_delta = (earliest_end - latest_start).seconds
#     overlap = max(0, delta)
#     overlap
#
#
# i=0


# df[(df.MMSI == 357147000)|(df.MMSI == 366760710)]
# df_sectors = df[()&()&()&()]
# temp_df =     df2[(df2.BaseDateTime > time_min)&(df2.BaseDateTime < time_max)]
# ships = df.MMSI.tolist()
# if len(ships) > 1
#     for ship in ships:

