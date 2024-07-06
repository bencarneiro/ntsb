#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"

python3 manage.py 2010_accident > /var/log/2010_accident.txt
python3 manage.py 2010_vehicle > /var/log/2010_vehicle.txt
python3 manage.py 2010_parkwork > /var/log/2010_parkwork.txt
python3 manage.py 2010_person > /var/log/2010_person.txt
python3 manage.py 2010_cevent > /var/log/2010_cevent.txt
python3 manage.py 2010_crashrf > /var/log/2010_crashrf.txt
python3 manage.py 2010_weather > /var/log/2010_weather.txt
python3 manage.py 2010_safetyeq > /var/log/2010_safetyeq.txt
python3 manage.py 2010_damage > /var/log/2010_damage.txt
python3 manage.py 2010_distract > /var/log/2010_distract.txt
python3 manage.py 2010_drimpair > /var/log/2010_drimpair.txt
python3 manage.py 2010_factor > /var/log/2010_factor.txt
python3 manage.py 2010_maneuver > /var/log/2010_maneuver.txt
python3 manage.py 2010_violatn > /var/log/2010_violatn.txt
python3 manage.py 2010_vision > /var/log/2010_vision.txt
python3 manage.py 2010_vehiclesf > /var/log/2010_vehiclesf.txt
python3 manage.py 2010_driverrf > /var/log/2010_driverrf.txt
python3 manage.py 2010_pvehiclesf > /var/log/2010_pvehiclesf.txt
python3 manage.py 2010_drugs > /var/log/2010_drugs.txt
python3 manage.py 2010_race > /var/log/2010_race.txt
python3 manage.py 2010_personrf > /var/log/2010_personrf.txt
python3 manage.py 2010_nmcrash > /var/log/2010_nmcrash.txt
python3 manage.py 2010_nmimpair > /var/log/2010_nmimpair.txt
python3 manage.py 2010_nmprior > /var/log/2010_nmprior.txt
