from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
import pandas as pd
from fatalities.models import CrashRelatedFactors, Accident
from fatalities.data_processing import crash_related_factor_converter
# 1975 - 1978 cf1, cf2, cf3

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        CrashRelatedFactors.objects.filter(accident__year=1978).delete()
        csv = pd.read_csv(f"{CSV_PATH}1978/ACCIDENT.CSV", encoding='latin-1')
        bulk_data_upload = []
        for x in csv.index:
            if x % 1000 == 999:
                print(new_factor_object)
                CrashRelatedFactors.objects.bulk_create(bulk_data_upload)
                bulk_data_upload = []
                print("WE HIT THE DB")
            accident = Accident.objects.get(year=1978, st_case=csv['ST_CASE'][x])
            number_of_factors_saved = 0
            for factor in ["CF1", "CF2", "CF3"]:
                st_case = str(csv['ST_CASE'][x])
                if len(st_case) == 5:
                    st_case = "0" + st_case
                # number_of_saved_factors = len(CrashRelatedFactors.objects.filter(accident=accident))
                new_factor_id = str(number_of_factors_saved + 1)
                while len(new_factor_id) < 3:
                    new_factor_id = "0" + new_factor_id
                primary_key = f"1978{st_case}{new_factor_id}"
                converted_factor_code = crash_related_factor_converter(csv[factor][x], 1978)
                if converted_factor_code:
                    number_of_factors_saved += 1
                    new_factor_object = CrashRelatedFactors(
                        id=primary_key,
                        accident=accident,
                        crash_related_factor=converted_factor_code
                    )
                    bulk_data_upload += [new_factor_object]
                    # data_to_save = {
                    #     "id": primary_key,
                    #     "accident": accident,
                    #     "crash_related_factor": converted_factor_code
                    # }
                    # print(data_to_save)
                    # CrashRelatedFactors.objects.create(**data_to_save)
        print(new_factor_object)
        CrashRelatedFactors.objects.bulk_create(bulk_data_upload)
        # bulk_data_upload = []
        print("WE HIT THE DB one final time")