from django.core.management.base import BaseCommand
from fatalities.models import Accident, Vehicle
from data.settings import CSV_PATH
import pandas as pd

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # one time operation to update data from 2023 - > 2024 schema
        # only necessary on the production build of the website, as the import scripts have been amended to support the new schema
        # You don't need to run this
        print("reversing crash type edits from 2023")
        Vehicle.objects.filter(crash_type=301).update(crash_type=50)
        Vehicle.objects.filter(crash_type=302).update(crash_type=51)
        Vehicle.objects.filter(crash_type=401).update(crash_type=68)
        Vehicle.objects.filter(crash_type=402).update(crash_type=69)
        Vehicle.objects.filter(crash_type=403).update(crash_type=70)
        Vehicle.objects.filter(crash_type=404).update(crash_type=71)
        Vehicle.objects.filter(crash_type=405).update(crash_type=72)
        Vehicle.objects.filter(crash_type=406).update(crash_type=73)
        Vehicle.objects.filter(crash_type=408).update(crash_type=76)
        Vehicle.objects.filter(crash_type=409).update(crash_type=77)
        Vehicle.objects.filter(crash_type=410).update(crash_type=78)
        Vehicle.objects.filter(crash_type=411).update(crash_type=79)
        Vehicle.objects.filter(crash_type=412).update(crash_type=80)
        Vehicle.objects.filter(crash_type=413).update(crash_type=81)
        Vehicle.objects.filter(crash_type=414).update(crash_type=82)
        Vehicle.objects.filter(crash_type=415).update(crash_type=83)
        Vehicle.objects.filter(crash_type=501).update(crash_type=86)
        Vehicle.objects.filter(crash_type=502).update(crash_type=87)
        Vehicle.objects.filter(crash_type=503).update(crash_type=88)
        Vehicle.objects.filter(crash_type=504).update(crash_type=89)
        Vehicle.objects.filter(crash_type=992).update(crash_type=92)
        Vehicle.objects.filter(crash_type=993).update(crash_type=93)
        Vehicle.objects.filter(crash_type=998).update(crash_type=98)
        Vehicle.objects.filter(crash_type=999).update(crash_type=99)

        print("overwriting 2023 crash type data")
        csv = pd.read_csv(f"{CSV_PATH}2023/FARS2023NationalCSV/vehicle.csv", encoding='latin-1')
        for x in csv.index:
            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            primary_key = f"2023{st_case}{veh_no}"
            vehicle = Vehicle.objects.get(id=int(primary_key))
            vehicle.crash_type = csv['ACC_TYPE'][x]
            vehicle.save()
            print(f"saved {primary_key}")
        