from django.core.management.base import BaseCommand
from fatalities.models import Person
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Person.objects.filter(month_of_death=0, accident__year=2008).update(month_of_death=88)
        test = Person.objects.filter(month_of_death=0)
        print(len(test))