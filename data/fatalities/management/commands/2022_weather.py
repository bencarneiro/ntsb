from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Weather, Accident

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Weather.objects.filter(accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/weather.csv", encoding='latin-1')
        for x in csv.index:
            accident = Accident.objects.get(st_case=csv['ST_CASE'][x])
            data_to_save = {
                "accident": accident,
                "atmospheric_condition": csv['WEATHER'][x]
            }
            print(data_to_save)
            Weather.objects.create(**data_to_save)