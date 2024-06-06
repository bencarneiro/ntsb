# [roadway.report](https:roadway.report)

This repo powers [roadway.report](https:roadway.report), a web application which can serve data on any traffic death in the USA since 1975


The data was interpreted mostly from [this manual](https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813556), published by the NHTSA

Project is built on PostGIS with Django/GeoDjango

[Here](https://roadway.report/schema) is a more compact look at the data model for the application

In the file data_dictionary.py, you can find a complete mapping of the government table/variable names to the more descriptive variable names used on roadway.report

If you want to run the application on your machine, 
requirements: django, geodjango, postgis/postgres, django-ninja, pydantic

Then run the ETL scripts to import data. In order for the import scripts to run correctly, they need to be in this order - This applies to any year of data importing

accident, create_datetimes, create_points, vehicle, parkwork, person, pbtype, cevent, crashrf, weather, vehiclesf, pvehiclesf, driverrf, damage, distract, drimpair, factor, maneuver, violatn, vision, personrf, drugs, race, nmcrash, nmimpair, nmdistract, nmprior, safetyeq
