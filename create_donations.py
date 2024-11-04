import csv
import json

donation_dates = []

output_donations = open("hub_owner_time_donations.json", "w", encoding='utf-8')

def write_record(person_id, hub_id, donation_date):
    record = {'donation_item_id': 40013, 'person_id': person_id, 'donation_date': donation_date, 'donation_qty': 5, 'time_value': 5, 'donor_hub_id': hub_id}
    json.dump(record, output_donations, ensure_ascii=False, indent=4)


with open('donation_dates.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # print(row)
        donation_dates.append(row[0])

# for date in donation_dates:
#     print(date)


# Data in owner_dates is hub_id, person_id, owner start date, owner end date, hub close date

with open('owner_dates.csv', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        # print(row[0])
        # print(row[1])
        # donation_dates.append(row[0])
        write_record(row[1], row[0], row[2])

output_donations.close()