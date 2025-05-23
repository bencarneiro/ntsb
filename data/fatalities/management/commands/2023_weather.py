from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import Weather, Accident

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        Weather.objects.filter(accident__year=2023).delete()
        csv = pd.read_csv(f"{CSV_PATH}2023/FARS2023NationalCSV/weather.csv", encoding='latin-1')
        for x in csv.index:
            accident = Accident.objects.get(year=2023, st_case=csv['ST_CASE'][x])

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            number_of_saved_weathers = len(Weather.objects.filter(accident=accident))
            new_weather_id = str(number_of_saved_weathers + 1)
            while len(new_weather_id) < 3:
                new_weather_id = "0" + new_weather_id
            primary_key = f"2023{st_case}{new_weather_id}"

            data_to_save = {
                "id": primary_key,
                "accident": accident,
                "atmospheric_condition": csv['WEATHER'][x]
            }
            print(data_to_save)
            Weather.objects.create(**data_to_save)