# Generated by Django 4.1.5 on 2024-07-11 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0023_alter_vehicle_cdl_endorsements_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="parked_vehicle_which_struck_non_motorist",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="parked_vehicle_which_struck_nonmotorist",
                to="fatalities.parkedvehicle",
            ),
        ),
    ]
