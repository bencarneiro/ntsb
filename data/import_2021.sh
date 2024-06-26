#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2021_accident > /var/log/2021_accident.txt
python3 manage.py 2021_vehicle > /var/log/2021_vehicle.txt
python3 manage.py 2021_parkwork > /var/log/2021_parkwork.txt
python3 manage.py 2021_person > /var/log/2021_person.txt
python3 manage.py 2021_cevent > /var/log/2021_cevent.txt
python3 manage.py 2021_crashrf > /var/log/2021_crashrf.txt
python3 manage.py 2021_weather > /var/log/2021_weather.txt
python3 manage.py 2021_pbtype > /var/log/2021_pbtype.txt
python3 manage.py 2021_safetyeq > /var/log/2021_safetyeq.txt
python3 manage.py 2021_damage > /var/log/2021_damage.txt
python3 manage.py 2021_distract > /var/log/2021_distract.txt
python3 manage.py 2021_drimpair > /var/log/2021_drimpair.txt
python3 manage.py 2021_factor > /var/log/2021_factor.txt
python3 manage.py 2021_maneuver > /var/log/2021_maneuver.txt
python3 manage.py 2021_violatn > /var/log/2021_violatn.txt
python3 manage.py 2021_vision > /var/log/2021_vision.txt
python3 manage.py 2021_vehiclesf > /var/log/2021_vehiclesf.txt
python3 manage.py 2021_driverrf > /var/log/2021_driverrf.txt
python3 manage.py 2021_pvehiclesf > /var/log/2021_pvehiclesf.txt
python3 manage.py 2021_drugs > /var/log/2021_drugs.txt
python3 manage.py 2021_race > /var/log/2021_race.txt
python3 manage.py 2021_personrf > /var/log/2021_personrf.txt
python3 manage.py 2021_nmcrash > /var/log/2021_nmcrash.txt
python3 manage.py 2021_nmimpair > /var/log/2021_nmimpair.txt
python3 manage.py 2021_nmdistract > /var/log/2021_nmdistract.txt
python3 manage.py 2021_nmprior > /var/log/2021_nmprior.txt
