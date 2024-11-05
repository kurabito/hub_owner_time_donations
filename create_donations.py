# import csv
import pandas as pd
import json

# donation_dates = []

def write_record(person_id, hub_id, donation_date):
    record = {'donation_item_id': 40013, 'person_id': person_id, 'donation_date': donation_date, 'donation_qty': 5, 'time_value': 5, 'donor_hub_id': hub_id}
    json.dump(record, output_donations, ensure_ascii=False, indent=4)

output_donations = open("hub_owner_time_donations.json", "w", encoding='utf-8')


# with open('donation_dates.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     for row in csv_reader:
#         if row[0] < '11/1/2024':
#             donation_dates.append(row[0])
#             print(row)


donation_dates = pd.read_csv("donation_dates.csv", parse_dates=["donation_date"])
# print(donation_dates)

# for date in donation_dates:
#     print(date)


# Data in owner_dates is hub_id, person_id, owner_start_date, owner_end_date, hub_close_ date

# with open('owner_dates.csv', encoding='utf-8-sig') as file:
#     csv_reader = csv.reader(file)
#     for row in csv_reader:
#         # print(row[0])
#         # print(row[1])
#         # donation_dates.append(row[0])
#         if row[2] != None:
#             for date in donation_dates:
#                 if date >= row[2]:
#                     # if row[3] == None and row[4] == None:
#                         # write_record(row[1], row[0], date)
#                         x = date


# owner_dates = pd.read_csv("owner_dates.csv", parse_dates=["owner_start_date", "owner_end_date", "hub_close_date"], dtype={'owner_start_date': 'datetime64[ns]', 'owner_end_date': 'datetime64[ns]', 'hub_close_date': 'datetime64[ns]'})
owner_dates = pd.read_csv("owner_dates.csv", parse_dates=["owner_start_date", "owner_end_date", "hub_close_date"])
# owner_dates = pd.read_csv("owner_dates.csv")
# Something about the end date column causes parse_dates to fail, fix it here
owner_dates['owner_end_date'] = pd.to_datetime(owner_dates['owner_end_date'], errors='coerce')
print(owner_dates)
for owner in owner_dates.itertuples():
    # print(owner)
    if not pd.isnull(owner.owner_start_date):
        # print(owner.owner_start_date)
        for date in donation_dates.itertuples():
            if not pd.isnull(owner.owner_end_date):
                if date.donation_date >= owner.owner_start_date and date.donation_date <= owner.owner_end_date and date.donation_date <= owner.hub_close_date:
                    # print(date.donation_date)
                    # print(type(date.donation_date))
                    # print('End date type: ')
                    # print(type(owner.owner_end_date))
                    # x = date
                    # write_record(owner.person_id, owner.hub_id, date.__str__())
                    write_record(owner.person_id, owner.hub_id, date.donation_date.__str__())


output_donations.close()