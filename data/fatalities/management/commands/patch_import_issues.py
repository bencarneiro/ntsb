from django.core.management.base import BaseCommand
from fatalities.models import Person, Vehicle, Accident, ParkedVehicle, Damage, Race


class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        nonmotorist_location_issues = Person.objects.filter(non_motorist_location=4)
        for x in nonmotorist_location_issues:
            x.non_motorist_location=9
            print(x.accident.year)
            x.save()
        nonmotorist_location_issues = Person.objects.filter(non_motorist_location=5)
        for x in nonmotorist_location_issues:
            x.non_motorist_location=10
            print(x.accident.year)
            x.save()
        nonmotorist_location_issues = Person.objects.filter(non_motorist_location=6)
        for x in nonmotorist_location_issues:
            x.non_motorist_location=21
            print(x.accident.year)
            x.save()
        first_harmful_event_issues = Accident.objects.filter(first_harmful_event=13)
        for y in first_harmful_event_issues:
            y.first_harmful_event = 12
            y.save()

        most_harmful_event_issues = Vehicle.objects.filter(most_harmful_event=13)
        for y in most_harmful_event_issues:
            y.most_harmful_event = 12
            y.save()

        most_harmful_event_issues = Vehicle.objects.filter(most_harmful_event=29)
        for y in most_harmful_event_issues:
            y.most_harmful_event = 31
            y.save()
        
        most_harmful_event_issues = Vehicle.objects.filter(most_harmful_event=0)
        for y in most_harmful_event_issues:
            y.most_harmful_event = 99
            print(y.accident.year)
            y.save()

        event_issues = Accident.objects.filter(first_harmful_event=29)
        print(event_issues.count())
        for x in event_issues:
            print(x.year)
            x.first_harmful_event=31
            x.save()

        route_signing_issues = Accident.objects.filter(route_signing=9)
        for z in route_signing_issues:
            z.route_signing=99
            z.save()

        vehicle_towed_issues = Vehicle.objects.filter(vehicle_towed=0)
        for v in vehicle_towed_issues:
            v.vehicle_towed = 8
            print(v.accident.year)
            v.save()
        
        impact_issues = Damage.objects.filter(area_of_impact=21)
        for i in impact_issues:
            i.area_of_impact = 99
            i.save()
            print(i.vehicle.accident.year)
        
        hispanic_issues = Person.objects.filter(hispanic=9)
        for h in hispanic_issues:
            h.hispanic=99
            print(h.accident.year)
            h.save()
        
        race_issues = Race.objects.filter(race=9)
        for r in race_issues:
            r.race = 99
            print(r.person.accident.year)
            r.save()