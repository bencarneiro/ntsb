from django.core.management.base import BaseCommand
from fatalities.models import InjuryAccident
# Example usage:


def get_collision_meaning(code):
    try:
        code = int(code)
    except:
        return code
    collision_codes = {
        1: "Pedestrian",
        2: "Pedalcyclist",
        3: "Railway train",
        4: "Animal",
        5: "Overturned",
        6: "Fixed Object",
        7: "Other Object",
        8: "Other non-collision",
        9: "Parked motor vehicle",
        10: "Turning",
        11: "Front to rear",
        12: "Sideswipe-same direction",
        13: "Sideswipe-opposite direction",
        14: "Front to front",
        15: "Angle",
        16: "Rear to side",
        17: "Rear to rear"
    }
    
    return collision_codes.get(code, "Unknown")

class Command(BaseCommand):
    def handle(self, *args, **kwasrgs):
        illinois_accidents = InjuryAccident.objects.filter(state_id=17)
        for crash in illinois_accidents:
            print(crash.id)
            print(crash.crash_type)
            print("became")
            crash.crash_type = get_collision_meaning(crash.crash_type)
            crash.save()
            print(crash.crash_type)