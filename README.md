# ntsb

this repo powers https://roadway.report

docs at https://roadway.report/v1/docs


This REPO is eventually going to contain a web application which can serve data on any traffic death in the USA since 1975

here are links to the meaning of all the 1s and 0s in the spreadsheets
Search for "FARS Analytical Users Manual, 1975-2022"

https://crashstats.nhtsa.dot.gov/#!/DocumentTypeList/23


In order for the import scripts to run correctly, they need to be in this order - This applies to any year of data importing

accident, create_datetimes, create_points, vehicle, parkwork, person, pbtype, cevent, crashrf, weather, vehiclesf, pvehiclesf, driverrf, damage, distract, drimpair, factor, maneuver, violatn, vision, personrf, drugs, race, nmcrash, nmimpair, nmdistract, nmprior, safetyeq
