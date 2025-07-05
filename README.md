# [roadway.report](https://roadway.report)

This repo powers [roadway.report](https://roadway.report), a web application in-development which will serve data on any traffic death in the USA since 1975

![Preview of roadway-report map](https://censusmaps.org/static/death.png)

I want people to build nice, interactive maps ontop of these APIS. This can support a nationwide vision-zero viewer.
Here's a crummy [proof of concept](https://roadway.report).

Or get data straight from the API via the [docs](https://roadway.report/v1/docs) and [TUTORIAL](https://roadway.report/api_tutorial_notebook).

The data was interpreted mostly from [this manual](https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813556), published by the NHTSA.

Based on this original data model:

![Screenshot from 2023-09-22 07-29-06](https://github.com/bencarneiro/ntsb/assets/63479105/52ab1a18-5d50-48c0-a416-cf2d4b148f4f)

Is now represented by a much more modern and descriptive [Schema](https://roadway.report/schema).

In the file `data_dictionary.py`, you can find a complete mapping of the government table/variable names to the more descriptive variable names used on roadway.report

## Instructions for running the application in development

Sorry folks, no docker here, but dependencies are pretty minimal. This is literally every command I had to run on a fresh install of debian to get this sucker up on my non-work machine.

```sh
sudo apt update
sudo apt install git
sudo apt install pip
sudo apt install postgresql-14
sudo apt install postgresql-14-postgis-3
```

Pop open postgres:

```sh
sudo -u postgres psql
```

And let's make a database:

```sh
CREATE DATABASE crash;
\c crash;
CREATE EXTENSION postgis;
CREATE USER app WITH PASSWORD 'assword';
GRANT ALL PRIVILEGES ON DATABASE crash TO app;
```

Clone the repo:

```sh
cd /path/to/where-you-want-the-application
git clone https://github.com/bencarneiro/ntsb.git
```

Get your python packages sorted:

_(Feel free to create a virtual environment here.)_

```sh
pip install django
pip install pandas
pip install pymysql
pip install django-extensions
pip install psycopg
pip install django-ninja
pip install folium
pip install geoip2
pip install googlemaps
pip install pillow
pip install qrcode
```

**Geo location:** Application uses IP addresses to find user-location and load the map.([Django docs on how this is set up](https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geoip2/)). [Download the geographies](https://drive.google.com/drive/folders/1JCmyvSZVb2vcpceOAUwhy8gh2tzo5ucB?usp=sharing) and then then make sure they line up with the GEOIP_PATH in settings.py
This doesn't really work in development anyway (you make requests both to-and-from 127.0.0.1) so the Geolocation from IP is bunk in dev.

Next, let's rip in some data, shall we?
[download this db dump](https://drive.google.com/file/d/1Q4yAmPdjduxtit8GTLbOQcyt9aSREyNt/view?usp=sharing), which contains a real copy of production (1.7 GB):

```sh
sudo -u postgres psql crash < db_backup_2025_07_02.sql
```

Then give it a boot:

```sh
python3 manage.py runserver
```

Then boot up the tile server:

```sh
cd fatalities/templates/static/tiles
http-server . --cors
```

and then try to access your server at http://127.0.0.1:8000.

## Contact

Feel free to reach out if something goes wrong ben@bencarneiro.com
