from django.core.management.base import BaseCommand
from data.settings import CSV_PATH

# import requests
import os
import zipfile, urllib.request, shutil



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # if the script breaks, just extract the files manually and restart the script from the right year

        if not os.path.exists("csvs"):
            os.mkdir("csvs")

        for year in range(1975, 2022):
            url = f"https://static.nhtsa.gov/nhtsa/downloads/FARS/{year}/National/FARS{year}NationalCSV.zip"
            if not os.path.exists(f"csvs/{year}"):
                os.mkdir(f"csvs/{year}")
            file_name = f"csvs/{year}/data{year}.zip"
            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                with zipfile.ZipFile(file_name) as zf:
                    zf.extractall(path=f"csvs/{year}")