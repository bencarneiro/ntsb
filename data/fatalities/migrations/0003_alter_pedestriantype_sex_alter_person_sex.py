# Generated by Django 4.1.5 on 2024-06-07 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0002_alter_person_at_work_alter_person_hispanic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedestriantype",
            name="sex",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "Male"),
                    (2, "Female"),
                    (3, "Other"),
                    (8, "Not Reported"),
                    (9, "Reported as Unknown"),
                ],
                default=8,
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="sex",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "Male"),
                    (2, "Female"),
                    (3, "Other"),
                    (8, "Not Reported"),
                    (9, "Reported as Unknown"),
                ],
                default=8,
            ),
        ),
    ]
