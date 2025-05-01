from django.core.management.base import BaseCommand
from fatalities.models import Accident, Vehicle
from data.settings import CSV_PATH

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # one time operation to update data from 2022 - > 2023 schema
        # only necessary on the production build of the website, as the import scripts have been amended to support the new schema
        # You don't need to run this
        Vehicle.objects.filter(crash_type=50).update(crash_type=301)
        Vehicle.objects.filter(crash_type=51).update(crash_type=302)
        Vehicle.objects.filter(crash_type=68).update(crash_type=401)
        Vehicle.objects.filter(crash_type=69).update(crash_type=402)
        Vehicle.objects.filter(crash_type=70).update(crash_type=403)
        Vehicle.objects.filter(crash_type=71).update(crash_type=404)
        Vehicle.objects.filter(crash_type=72).update(crash_type=405)
        Vehicle.objects.filter(crash_type=73).update(crash_type=406)
        Vehicle.objects.filter(crash_type=76).update(crash_type=408)
        Vehicle.objects.filter(crash_type=77).update(crash_type=409)
        Vehicle.objects.filter(crash_type=78).update(crash_type=410)
        Vehicle.objects.filter(crash_type=79).update(crash_type=411)
        Vehicle.objects.filter(crash_type=80).update(crash_type=412)
        Vehicle.objects.filter(crash_type=81).update(crash_type=413)
        Vehicle.objects.filter(crash_type=82).update(crash_type=414)
        Vehicle.objects.filter(crash_type=83).update(crash_type=415)
        Vehicle.objects.filter(crash_type=86).update(crash_type=501)
        Vehicle.objects.filter(crash_type=87).update(crash_type=502)
        Vehicle.objects.filter(crash_type=88).update(crash_type=503)
        Vehicle.objects.filter(crash_type=89).update(crash_type=504)
        Vehicle.objects.filter(crash_type=92).update(crash_type=992)
        Vehicle.objects.filter(crash_type=93).update(crash_type=993)
        Vehicle.objects.filter(crash_type=99).update(crash_type=998)
        Vehicle.objects.filter(crash_type=99).update(crash_type=999)