from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import ParkedVehicle, Vehicle, Accident, VehicleSequenceOfEvents
from fatalities.data_processing import soe_converter
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        VehicleSequenceOfEvents.objects.filter(vehicle__accident__year=2004).delete()
        VehicleSequenceOfEvents.objects.filter(parked_vehicle__accident__year=2004).delete()

        # csv = pd.read_csv(f"{CSV_PATH}2004/FARS2004NationalCSV/CEVENT.CSV", encoding='latin-1')
        csv = pd.read_csv(f"{CSV_PATH}2004/VEHICLE.CSV", encoding='latin-1')
        for x in csv.index:
            veh_no = str(csv['VEH_NO'][x])
            while len(veh_no) < 3:
                veh_no = "0" + veh_no
            vehicle = Vehicle.objects.get(accident__year=2004, accident__st_case=csv['ST_CASE'][x], vehicle_number=csv['VEH_NO'][x])
            for event in ['SEQ1', "SEQ2", "SEQ3", "SEQ4", "SEQ5", "SEQ6"]:
                st_case = str(csv['ST_CASE'][x])
                if len(st_case) == 5:
                    st_case = "0" + st_case
                number_of_saved_events = len(VehicleSequenceOfEvents.objects.filter(vehicle=vehicle))
                new_event_id = str(number_of_saved_events + 1)
                while len(new_event_id) < 3:
                    new_event_id = "0" + new_event_id
                primary_key = f"2004{st_case}{veh_no}{new_event_id}"
                soe = soe_converter(csv[event][x], 2004)
                data_to_save = {
                    "id": primary_key,
                    "vehicle": vehicle,
                    "vehicle_event_number": int(new_event_id),
                    "sequence_of_events": soe
                }
                if soe:
                    print(data_to_save)
                    VehicleSequenceOfEvents.objects.create(**data_to_save)
                # break
