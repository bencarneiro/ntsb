from django.core.management.base import BaseCommand
from data.settings import CSV_PATH


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print(args)
        print(kwargs)