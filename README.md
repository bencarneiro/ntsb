# [roadway.report](https://roadway.report)

This repo powers [roadway.report](https://roadway.report), a web application in-development which will serve data on any traffic death in the USA since 1975

I want people to build nice, interactive maps ontop of these APIS. This can support a nationwide vision-zero viewer
Here's a crummy [proof of concept](https://roadway.report/map)

The data was interpreted mostly from [this manual](https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813556), published by the NHTSA

Based on this original data model

![Screenshot from 2023-09-22 07-29-06](https://github.com/bencarneiro/ntsb/assets/63479105/52ab1a18-5d50-48c0-a416-cf2d4b148f4f)

Is now represented by a much more modern and descriptive [Schema](https://roadway.report/schema)

In the file data_dictionary.py, you can find a complete mapping of the government table/variable names to the more descriptive variable names used on roadway.report

If you want to run the application on your machine, 
requirements: django, geodjango, postgis/postgres, django-ninja, pydantic

Then run the ETL scripts to import data. In order for the import scripts to run correctly, they need to be in this order - This applies to any year of data importing

accident, create_datetimes, create_points, vehicle, parkwork, person, pbtype, cevent, crashrf, weather, vehiclesf, pvehiclesf, driverrf, damage, distract, drimpair, factor, maneuver, violatn, vision, personrf, drugs, race, nmcrash, nmimpair, nmdistract, nmprior, safetyeq

