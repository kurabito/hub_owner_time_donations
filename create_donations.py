import datetime
import pandas as pd
import json

output_donations = open("hub_owner_time_donations.json", "w", encoding='utf-8')

output_report = open("hub_owner_time_donations_report.txt", "w", encoding='utf-8')

def write_record(person_id, hub_id, donation_date):
    record = {'donation_item_id': 40013, 'person_id': person_id, 'donation_date': donation_date, 'donation_qty': 5, 'time_value': 5, 'donor_hub_id': hub_id}
    json.dump(record, output_donations, ensure_ascii=False, indent=4)

def write_report(person_id, hub_id, donation_date):
    line = 'person_id: ' + person_id.__str__() + ', donation_date: ' + donation_date.__str__() + ', hub_id: ' + hub_id.__str__() + '\n'
    output_report.writelines(line)

donation_dates = pd.read_csv("donation_dates.csv", parse_dates=["donation_date"])

# Data in owner_dates is hub_id, person_id, owner_start_date, owner_end_date, hub_close_ date
owner_dates = pd.read_csv("owner_dates.csv", parse_dates=["owner_start_date", "owner_end_date", "hub_close_date"])

# Something about the end date column causes parse_dates to fail, so fix it here
owner_dates['owner_end_date'] = pd.to_datetime(owner_dates['owner_end_date'], errors='coerce')

for owner in owner_dates.itertuples():
    end_date = datetime.datetime.now()
    if not pd.isna(owner.owner_end_date):
        end_date = owner.owner_end_date
    if not pd.isna(owner.hub_close_date):
        if owner.hub_close_date < end_date:
            end_date = owner.hub_close_date
        
    for date in donation_dates.itertuples():
        if date.donation_date >= owner.owner_start_date and date.donation_date <= end_date:
            write_record(owner.person_id, owner.hub_id, date.donation_date.__str__())
            write_report(owner.person_id, owner.hub_id, date.donation_date.__str__())

output_donations.close()