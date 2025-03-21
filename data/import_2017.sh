#!/bin/sh
export CSV_PATH="/root/ntsb/data/csvs/"
python3 manage.py 2017_accident > /var/log/2017_accident.txt
python3 manage.py 2017_vehicle > /var/log/2017_vehicle.txt
python3 manage.py 2017_parkwork > /var/log/2017_parkwork.txt
python3 manage.py 2017_person > /var/log/2017_person.txt
python3 manage.py 2017_cevent > /var/log/2017_cevent.txt
python3 manage.py 2017_crashrf > /var/log/2017_crashrf.txt
python3 manage.py 2017_weather > /var/log/2017_weather.txt
python3 manage.py 2018_pbtype > /var/log/2018_pbtype.txt
python3 manage.py 2018_safetyeq > /var/log/2018_safetyeq.txt
python3 manage.py 2017_pbtype > /var/log/2017_pbtype.txt
python3 manage.py 2017_safetyeq > /var/log/2017_safetyeq.txt
python3 manage.py 2017_damage > /var/log/2017_damage.txt
python3 manage.py 2017_distract > /var/log/2017_distract.txt
python3 manage.py 2017_drimpair > /var/log/2017_drimpair.txt
python3 manage.py 2017_factor > /var/log/2017_factor.txt
python3 manage.py 2017_maneuver > /var/log/2017_maneuver.txt
python3 manage.py 2017_violatn > /var/log/2017_violatn.txt
python3 manage.py 2017_vision > /var/log/2017_vision.txt
python3 manage.py 2017_vehiclesf > /var/log/2017_vehiclesf.txt
python3 manage.py 2017_driverrf > /var/log/2017_driverrf.txt
python3 manage.py 2017_pvehiclesf > /var/log/2017_pvehiclesf.txt
python3 manage.py 2017_drugs > /var/log/2017_drugs.txt
python3 manage.py 2017_race > /var/log/2017_race.txt
python3 manage.py 2017_personrf > /var/log/2017_personrf.txt
python3 manage.py 2017_nmcrash > /var/log/2017_nmcrash.txt
python3 manage.py 2017_nmimpair > /var/log/2017_nmimpair.txt
python3 manage.py 2017_nmprior > /var/log/2017_nmprior.txt
