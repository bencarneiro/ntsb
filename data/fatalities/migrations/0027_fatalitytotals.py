# Generated by Django 4.1.5 on 2024-07-25 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0026_alter_driverrelatedfactor_driver_related_factor"),
    ]

    operations = [
        migrations.CreateModel(
            name="FatalityTotals",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_fatalities", models.PositiveSmallIntegerField(default=1)),
                ("vehicle_fatalities", models.PositiveSmallIntegerField(default=0)),
                ("nonmotorist_fatalities", models.PositiveSmallIntegerField(default=0)),
                ("driver_fatalities", models.PositiveSmallIntegerField(default=0)),
                ("passenger_fatalities", models.PositiveSmallIntegerField(default=0)),
                (
                    "parked_vehicle_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                (
                    "nonmotorized_transport_device_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                ("pedestrian_fatalities", models.PositiveSmallIntegerField(default=0)),
                ("bicycle_fatalities", models.PositiveSmallIntegerField(default=0)),
                (
                    "pedalcyclist_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                (
                    "personal_conveyance_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                (
                    "unknown_vehicle_occupant_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                (
                    "person_in_building_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                (
                    "unknown_nonmotorist_fatalities",
                    models.PositiveSmallIntegerField(default=0),
                ),
                (
                    "accident",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="fatalities.accident",
                    ),
                ),
            ],
            options={
                "db_table": "fatality_totals",
                "managed": True,
            },
        ),
    ]
