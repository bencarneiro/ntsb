#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2022_accident > /var/log/2022_accident.txt
python3 manage.py 2022_vehicle > /var/log/2022_vehicle.txt
python3 manage.py 2022_parkwork > /var/log/2022_parkwork.txt
python3 manage.py 2022_person > /var/log/2022_person.txt
python3 manage.py 2022_cevent > /var/log/2022_cevent.txt
python3 manage.py 2022_crashrf > /var/log/2022_crashrf.txt
python3 manage.py 2022_weather > /var/log/2022_weather.txt
python3 manage.py 2022_pbtype > /var/log/2022_pbtype.txt
python3 manage.py 2022_safetyeq > /var/log/2022_safetyeq.txt
python3 manage.py 2022_damage > /var/log/2022_damage.txt
python3 manage.py 2022_distract > /var/log/2022_distract.txt
python3 manage.py 2022_drimpair > /var/log/2022_drimpair.txt
python3 manage.py 2022_factor > /var/log/2022_factor.txt
python3 manage.py 2022_maneuver > /var/log/2022_maneuver.txt
python3 manage.py 2022_violatn > /var/log/2022_violatn.txt
python3 manage.py 2022_vision > /var/log/2022_vision.txt
python3 manage.py 2022_vehiclesf > /var/log/2022_vehiclesf.txt
python3 manage.py 2022_driverrf > /var/log/2022_driverrf.txt
python3 manage.py 2022_pvehiclesf > /var/log/2022_pvehiclesf.txt
python3 manage.py 2022_drugs > /var/log/2022_drugs.txt
python3 manage.py 2022_race > /var/log/2022_race.txt
python3 manage.py 2022_personrf > /var/log/2022_personrf.txt
python3 manage.py 2022_nmcrash > /var/log/2022_nmcrash.txt
python3 manage.py 2022_nmimpair > /var/log/2022_nmimpair.txt
python3 manage.py 2022_nmdistract > /var/log/2022_nmdistract.txt
python3 manage.py 2022_nmprior > /var/log/2022_nmprior.txt
