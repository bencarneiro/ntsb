from django.core.management.base import BaseCommand
from data.settings import ACCIDENT_CSV_PATHS
from fatalities.models import Accident
import pandas as pd

def stringify_county_code(state_id, county_id):
    state_id = str(state_id)
    while len(state_id) < 2:
        state_id = "0" + state_id
    county_id = str(county_id)
    while len(county_id) < 3:
        county_id = "0" + county_id

    return state_id + county_id

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        result_dict = {}
        for year in range(1980,2024):
            accident_csv = pd.read_csv(f"/home/tonydeals/app/ntsb/data/csvs/{ACCIDENT_CSV_PATHS[year]}", encoding="latin-1")
            countyless_crashes = Accident.objects.filter(year=year, county__isnull=True)
            for crash in countyless_crashes:
                st_case = str(crash.id)[4:]
                csv_crash = accident_csv[accident_csv['ST_CASE']==int(st_case)].reset_index()
                state_id = csv_crash['STATE'][0]
                county_id = csv_crash['COUNTY'][0]
                full_county_id = stringify_county_code(state_id, county_id)
                if full_county_id in result_dict:
                    result_dict[full_county_id] += 1
                else:
                    result_dict[full_county_id] = 1
        print(result_dict)