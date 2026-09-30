from django.core.management.base import BaseCommand
from fatalities.models import Person, Vehicle, Accident, ParkedVehicle


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
