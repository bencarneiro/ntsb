# Generated by Django 4.1.5 on 2024-05-24 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0006_person_parked_vehicle"),
    ]

    operations = [
        migrations.AddField(
            model_name="crashevent",
            name="parked_vehicle_1",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="crash_event_parked_vehicle_1",
                to="fatalities.parkedvehicle",
            ),
        ),
        migrations.AddField(
            model_name="crashevent",
            name="parked_vehicle_2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="crash_event_parked_vehicle_2",
                to="fatalities.parkedvehicle",
            ),
        ),
    ]