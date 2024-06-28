from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import CrashRelatedFactors, Accident
from fatalities.data_processing import crash_related_factor_converter
# 1975 - 2019 cf1, cf2, cf3

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        CrashRelatedFactors.objects.filter(accident__year=2020).delete()
        csv = pd.read_csv(f"{CSV_PATH}2020/FARS2020NationalCSV/crashrf.csv", encoding='latin-1')
        for x in csv.index:
            
            accident = Accident.objects.get(year=2020, st_case=csv['ST_CASE'][x])

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            number_of_saved_factors = len(CrashRelatedFactors.objects.filter(accident=accident))
            new_factor_id = str(number_of_saved_factors + 1)
            while len(new_factor_id) < 3:
                new_factor_id = "0" + new_factor_id
            primary_key = f"2020{st_case}{new_factor_id}"

            data_to_save = {
                "id": primary_key,
                "accident": accident,
                "crash_related_factor": crash_related_factor_converter(csv['CRASHRF'][x], 2020)
            }
            print(data_to_save)
            CrashRelatedFactors.objects.create(**data_to_save)