from django.core.management.base import BaseCommand
from fatalities.models import Accident, FatalityTotals

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        FatalityTotals.objects.all().delete()
        for year in range(2001,2024):
            for a in Accident.objects.filter(year=year):
                people = a.person_set.filter(injury_severity=4)

                total_fatalities = 0
                vehicle_fatalities = 0
                nonmotorist_fatalities = 0

                # 5,10,19
                ped_fatalities = 0
                # 6,7,8
                bike_fatalities = 0

                #1
                driver_fatalities = 0
                #2
                passenger_fatalities = 0
                #3
                parked_vehicle_fatalities = 0
                #4
                nonmotorized_transport_device_fatalities = 0
                #5
                pedestrian_fatalities = 0
                #6
                bicycle_fatalities = 0
                #7
                pedalcyclist_fatalities = 0
                #8
                personal_conveyance_fatalities = 0
                #9
                unknown_vehicle_occupant_fatalities = 0
                # 10
                person_in_building_fatalities = 0
                # 19
                unknown_nonmotorist_fatalities = 0
                for p in people:
                    total_fatalities += 1
                    if p.person_type == 1:
                        vehicle_fatalities += 1
                        driver_fatalities += 1
                    if p.person_type == 2:
                        vehicle_fatalities += 1
                        passenger_fatalities += 1
                    if p.person_type == 3:
                        vehicle_fatalities += 1
                        parked_vehicle_fatalities += 1
                    if p.person_type == 4:
                        vehicle_fatalities += 1
                        nonmotorized_transport_device_fatalities += 1
                    if p.person_type == 5:
                        nonmotorist_fatalities += 1
                        ped_fatalities += 1
                        pedestrian_fatalities += 1
                    if p.person_type == 6:
                        nonmotorist_fatalities += 1
                        bike_fatalities += 1
                        bicycle_fatalities += 1
                    if p.person_type == 7:
                        nonmotorist_fatalities += 1
                        bike_fatalities += 1
                        pedalcyclist_fatalities += 1
                    if p.person_type == 8:
                        nonmotorist_fatalities += 1
                        bike_fatalities += 1
                        personal_conveyance_fatalities += 1
                    if p.person_type == 9:
                        vehicle_fatalities += 1
                        unknown_vehicle_occupant_fatalities += 1
                    if p.person_type == 10:
                        nonmotorist_fatalities += 1
                        ped_fatalities += 1
                        person_in_building_fatalities += 1
                    if p.person_type == 19:
                        nonmotorist_fatalities += 1
                        ped_fatalities += 1
                        unknown_nonmotorist_fatalities += 1
                dict = {
                    "accident": a,
                    "total_fatalities": total_fatalities,
                    "vehicle_fatalities": vehicle_fatalities,
                    "nonmotorist_fatalities": nonmotorist_fatalities,
                    "ped_fatalities": ped_fatalities,
                    "bike_fatalities": bike_fatalities,
                    "driver_fatalities": driver_fatalities,
                    "passenger_fatalities": passenger_fatalities,
                    "parked_vehicle_fatalities": parked_vehicle_fatalities,
                    "nonmotorized_transport_device_fatalities": nonmotorized_transport_device_fatalities,
                    "pedestrian_fatalities": pedestrian_fatalities,
                    "bicycle_fatalities": bicycle_fatalities,
                    "pedalcyclist_fatalities": pedalcyclist_fatalities,
                    "personal_conveyance_fatalities": personal_conveyance_fatalities,
                    "unknown_vehicle_occupant_fatalities": unknown_vehicle_occupant_fatalities,
                    "person_in_building_fatalities": person_in_building_fatalities,
                    "unknown_nonmotorist_fatalities": unknown_nonmotorist_fatalities
                }
                FatalityTotals.objects.create(**dict)
                print(a.id)

