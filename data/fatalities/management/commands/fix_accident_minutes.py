from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import Accident, City, County, State
from fatalities.data_processing import get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        csv = pd.read_csv(f"{CSV_PATH}2022/FARS2022NationalCSV/FARS2022NationalCSV/accident.csv", encoding='latin-1')
        for x in csv.index:
            a = Accident.objects.get(st_case=csv['ST_CASE'][x])
            a.minute = csv['MINUTE'][x]
            print(f"wrote minute {csv['MINUTE'][x]} for case #{csv['ST_CASE'][x]}")
            a.save()