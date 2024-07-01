from django.core.management.base import BaseCommand
from data.settings import CSV_PATH
from fatalities.models import ParkedVehicle, Vehicle, Accident, CrashEvent
from fatalities.data_processing import FARS_DATA_CONVERTERS, get_data_source
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        CrashEvent.objects.filter(accident__year=2018).delete()
        model_fields =  [ "crash_event_number",
             "area_of_impact_1",
             "area_of_impact_2",
             "sequence_of_events"]

        csv = pd.read_csv(f"{CSV_PATH}2018/CEvent.CSV", encoding='latin-1')
        
        for x in csv.index:

            accident = Accident.objects.get(year=2018, st_case=csv['ST_CASE'][x])

            st_case = str(csv['ST_CASE'][x])
            if len(st_case) == 5:
                st_case = "0" + st_case
            number_of_saved_events = len(CrashEvent.objects.filter(accident=accident))
            new_event_id = str(number_of_saved_events + 1)
            while len(new_event_id) < 3:
                new_event_id = "0" + new_event_id
            primary_key = f"2018{st_case}{new_event_id}"
  
            data_to_save = {
                "id": primary_key,
                "accident": accident,
            }
            try:
                vehicle_1 = Vehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER1'][x])
            except:
                vehicle_1 = None
            data_to_save['vehicle_1'] = vehicle_1
            try:
                parked_vehicle_1 = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER1'][x])
            except:
                parked_vehicle_1 = None
            data_to_save['parked_vehicle_1'] = parked_vehicle_1
            try:
                vehicle_2 = Vehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER2'][x])
            except:
                vehicle_2 = None
            data_to_save['vehicle_2'] = vehicle_2
            try:
                parked_vehicle_2 = ParkedVehicle.objects.get(accident=accident, vehicle_number=csv['VNUMBER2'][x])
            except:
                parked_vehicle_2 = None
            data_to_save['parked_vehicle_2'] = parked_vehicle_2

            for model_field_name in model_fields:
                data_source = get_data_source("crash_event." + model_field_name, 2018)
                if data_source:
                    csv_field_name = data_source.split(".")[1]
                    data_converter_function = FARS_DATA_CONVERTERS["crash_event." + model_field_name]
                    data_to_save[model_field_name] = data_converter_function(csv[csv_field_name][x], 2018)
            print(data_to_save)
            CrashEvent.objects.create(**data_to_save)
            # break
