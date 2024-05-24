from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import CrashRelatedFactors, Accident

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        CrashRelatedFactors.objects.filter(accident__year=2022).delete()
        csv = pd.read_csv("/home/tonydeals/app/ntsb/data/csvs/2022/crashrf.csv", encoding='latin-1')
        for x in csv.index:
            accident = Accident.objects.get(st_case=csv['ST_CASE'][x])
            data_to_save = {
                "accident": accident,
                "crash_related_factor": csv['CRASHRF'][x]
            }
            print(data_to_save)
            CrashRelatedFactors.objects.create(**data_to_save)