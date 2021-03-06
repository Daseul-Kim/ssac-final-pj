# import

import pandas as pd
import numpy as np

# read data

data = pd.read_csv("data/hotel_bookings.csv")

# change month string to int

data['arrival_date_month'] = data['arrival_date_month'].replace('January', 1)
data['arrival_date_month'] = data['arrival_date_month'].replace('February', 2)
data['arrival_date_month'] = data['arrival_date_month'].replace('March', 3)
data['arrival_date_month'] = data['arrival_date_month'].replace('April', 4)
data['arrival_date_month'] = data['arrival_date_month'].replace('May', 5)
data['arrival_date_month'] = data['arrival_date_month'].replace('June', 6)
data['arrival_date_month'] = data['arrival_date_month'].replace('July', 7)
data['arrival_date_month'] = data['arrival_date_month'].replace('August', 8)
data['arrival_date_month'] = data['arrival_date_month'].replace('September', 9)
data['arrival_date_month'] = data['arrival_date_month'].replace('October', 10)
data['arrival_date_month'] = data['arrival_date_month'].replace('November', 11)
data['arrival_date_month'] = data['arrival_date_month'].replace('December', 12)

# make change_room as boolean
data['change_room'] = 0
data.loc[data['assigned_room_type'] != data['reserved_room_type'], 'change_room'] = 1


# vertify family or not
data['group_total'] = data['adults'] + data['children'] + data['babies']

num1 = data[data['group_total'] == 0].index
data = data.drop(num1)

data['is_group'] = 0
data.loc[data['group_total'] >= 3, 'is_group'] = 1
data.loc[(data['children'] != 0) | (data['babies'] != 0) & (data['adults'] != 0), 'is_group'] = 1


# divide leadtime to lead-term
data.loc[data['lead_time'] <= 30, 'lead_term'] = 1
data.loc[(data['lead_time'] > 30) & (data['lead_time'] <= 90), 'lead_term'] = 2
data.loc[(data['lead_time'] > 90) & (data['lead_time'] <= 180), 'lead_term'] = 3
data.loc[(data['lead_time'] > 180) & (data['lead_time'] <= 365), 'lead_term'] = 4
data.loc[(data['lead_time'] > 365), 'lead_term'] = 5


# divide adr ro adr-section
num2 = data['adr']._get_numeric_data()
num2[num2 < 0] = 0

data.loc[data['adr'] <= 50, 'adr_term'] = 1
data.loc[(data['adr'] > 50) & (data['adr'] <= 75), 'adr_term'] = 2
data.loc[(data['adr'] > 75) & (data['adr'] <= 100), 'adr_term'] = 3
data.loc[(data['adr'] > 100) & (data['adr'] <= 125), 'adr_term'] = 4
data.loc[(data['adr'] > 125), 'adr_term'] = 5


# make precan_bool(pre-cancellation) as boolean
data['precan_bool'] = 1
data.loc[data['previous_cancellations'] == 0, 'precan_bool'] = 0

# make packace as boolean
data.loc[data["distribution_channel"]=='Direct','Package(bool)'] = 0
data.loc[data["distribution_channel"]!='Direct','Package(bool)'] = 1
data.loc[data["distribution_channel"]=='Undefined','Package(bool)'] = np.nan


# make parkinglot(required car parking spaces) as beelean
data.loc[data['required_car_parking_spaces'] == 0, 'parkinglot'] = 0
data.loc[data['required_car_parking_spaces'] > 0,'parkinglot'] = 1

# export to csv
data.to_csv('data/hotel_bookings_data_preprocess.csv')


# classify resort hotel and city hotel
data = data[['hotel', 'is_canceled', 'arrival_date_year', 'arrival_date_month',
      'market_segment', 'change_room', 'is_group', 'lead_term', 'precan_bool', 'adr_term']]

resort = data['hotel'] == 'Resort Hotel'
resort_data = data[resort]

city = data['hotel'] == 'City Hotel'
city_data = data[city]

resort_data = resort_data.drop('hotel', axis=1)
city_data = city_data.drop('hotel', axis=1)
city_data = city_data.reset_index(drop=True)

resort_data.to_csv('data/resort_data_p.csv')
city_data.to_csv('data/city_data_p.csv')





