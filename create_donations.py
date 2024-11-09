import datetime
import pandas as pd
import json

output_donations = open("hub_owner_time_donations.json", "w", encoding='utf-8')

output_report = open("hub_owner_time_donations_report.txt", "w", encoding='utf-8')

def write_record(person_id, hub_id, donation_date_id, donation_date, other):
    record = {'donation_item_id': 40013, 'person_id': person_id, 'check_in_date_id': donation_date_id, 'donation_date': donation_date, 'donation_qty': 5, 'time_value': 5, 'hub_id': hub_id, 'donor_hub_id': hub_id, 'donation_other': other}
    json.dump(record, output_donations, ensure_ascii=False, indent=4)

def write_report_line(person_id, hub, start_date, end_date):
    start = start_date.strftime('%Y-%m-%d')
    end = end_date.strftime('%Y-%m-%d')
    line = 'person_id: ' + person_id.__str__() + ', hub: ' + hub + ', donation dates: ' + start + ' - ' + end + '\n'
    output_report.writelines(line)

donation_dates = pd.read_csv("donation_dates.csv", parse_dates=["check_in_date_date"])

# Data in owner_dates is hub_id, person_id, owner_start_date, owner_end_date, hub_close_ date, primary_area, neighborhood
owner_dates = pd.read_csv("owner_dates.csv", parse_dates=["owner_start_date", "owner_end_date", "hub_close_date"], dtype={'neighborhood': str})

# Something about the end date column causes parse_dates to fail, so fix it here
owner_dates['owner_end_date'] = pd.to_datetime(owner_dates['owner_end_date'], errors='coerce')

# neighborhood gets interpreted as float due to empty values, force to string
owner_dates['neighborhood'] = owner_dates['neighborhood'].astype(str)

# print(owner_dates)

for owner in owner_dates.itertuples():
    end_date = datetime.datetime(2024,6,23)
    if not pd.isna(owner.owner_end_date):
        end_date = owner.owner_end_date
    if not pd.isna(owner.hub_close_date):
        if owner.hub_close_date < end_date:
            end_date = owner.hub_close_date

    hub_name = owner.primary_area
    if not owner.neighborhood == 'nan':
        hub_name += ' - ' + owner.neighborhood
        
    for date in donation_dates.itertuples():
        if date.check_in_date_date >= owner.owner_start_date and date.check_in_date_date <= end_date:
            write_record(owner.person_id, owner.hub_id, date.check_in_date_id, date.check_in_date_date.__str__(), 'Hub: ' + hub_name)

    write_report_line(owner.person_id, str(owner.hub_id) + ' ' + hub_name, owner.owner_start_date, end_date)

output_donations.close()