# Generated by Django 4.1.5 on 2024-07-02 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0018_alter_personrelatedfactor_person_related_factor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="drugs",
            name="drug_test_type",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "Test Not Given"),
                    (1, "Whole Blood"),
                    (2, "Urine"),
                    (3, "Both Blood and Urine Tests"),
                    (11, "Blood Plasma/Serum"),
                    (12, "Blood Clot"),
                    (13, "Oral Fluids"),
                    (14, "Vitreous"),
                    (15, "Liver"),
                    (96, "Not Reported"),
                    (97, "Unknown Specimen"),
                    (98, "Other Specimen"),
                    (99, "Reported as Unknown if Tested"),
                ],
                default=0,
            ),
        ),
    ]