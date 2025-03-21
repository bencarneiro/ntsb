# Generated by Django 4.1.5 on 2024-06-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0006_alter_vehicle_ncsa_make"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="vehicle_configuration",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Not Applicable"),
                    (1, "Single-Unit Truck (2 Axles and GVWR More Than 10,000 lbs)"),
                    (2, "Single-Unit Truck (3 or More Axles)"),
                    (3, "Single-Unit Truck (Unknown Number of Axles, Tires)"),
                    (4, "Truck Pulling Trailer(s)"),
                    (5, "Truck Tractor (Bobtail)"),
                    (6, "Truck Tractor/Semi-Trailer"),
                    (7, "Truck Tractor/Double"),
                    (8, "Truck Tractor/Triple"),
                    (
                        10,
                        "Vehicle 10,000 lbs. or Less Placarded for Hazardous Materials",
                    ),
                    (19, "Vehicle More Than 10,000 lbs., Other"),
                    (20, "Bus/Large Van (Seats for 9-15 Occupants, Including Driver)"),
                    (
                        21,
                        "Bus (Seats for More Than 15 Occupants, Including Driver, 2010-Later)",
                    ),
                    (
                        70,
                        "Light Truck (Van, Mini-Van, Panel, Pickup, Sport Utility Vehicle Displaying a Hazardous Materials Placard)",
                    ),
                    (
                        80,
                        "Passenger Car (Only When Displaying a Hazardous Materials Placard)",
                    ),
                    (88, "Qualifying Vehicle, Unknown Configuration"),
                    (98, "Not Reported (2010-2012)"),
                    (99, "Unknown (Reported as Unknown, 2018-2019)"),
                ],
                default=0,
            ),
        ),
    ]
