from django.core.management.base import BaseCommand
import pandas as pd
from fatalities.models import Accident

def get_accident_datetime(a):
    year = str(a.year)
    month = str(a.month)
    if len(str(a.month)) == 1:
        month = "0" + str(a.month)
    day = str(a.day)
    if len(str(a.day)) == 1:
        day = "0" + str(a.day)
    hour = str(a.hour)
    if len(str(a.hour)) == 1:
        hour = "0" + str(a.hour)
    minute = str(a.minute)
    if len(str(a.minute)) == 1:
        minute = "0" + str(a.minute)
    if month == "99":
        return f"{year}-01-01 00:00:00Z-00+0000", True
    if day == "99":
        return f"{year}-{month}-01 00:00:00+0000", True
    if hour == "99":
        return f"{year}-{month}-{day} 00:00:00+0000", True
    if minute == "99":
        return f"{year}-{month}-{day} {hour}:00:00+0000", False
    return f"{year}-{month}-{day} {hour}:{minute}:00+0000", False


class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        counter = 0
        for a in Accident.objects.all().order_by("st_case"):
            counter +=1
            print(a.month)
            print(a.day)
            print(a.year)
            print(a.hour)
            print(a.minute)
            dt = get_accident_datetime(a)
            print(dt)
            a.datetime = dt[0]
            a.datetime_is_estimated = dt[1]
            a.save()
