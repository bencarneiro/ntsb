# Generated by Django 4.1.5 on 2024-07-05 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0021_comment_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="damage",
            name="area_of_impact",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "1 O'Clock"),
                    (2, "2 O'Clock"),
                    (3, "3 O'Clock"),
                    (4, "4 O'Clock"),
                    (5, "5 O'Clock"),
                    (6, "6 O'Clock"),
                    (7, "7 O'Clock"),
                    (8, "8 O'Clock"),
                    (9, "9 O'Clock"),
                    (10, "10 O'Clock"),
                    (11, "11 O'Clock"),
                    (12, "12 O'Clock"),
                    (13, "Top"),
                    (14, "Undercarriage"),
                    (15, "No Damage"),
                    (16, "Override"),
                    (17, "Underride"),
                    (18, "Cargo/Vehicle Parts Set-in-Motion"),
                    (19, "Other Objects or Person Set-in-Motion"),
                    (
                        20,
                        "Object Set in Motion, Unknown if Cargo/Vehicle Parts or Other",
                    ),
                    (61, "Left"),
                    (62, "Left-Front Side"),
                    (63, "Left-Back Side"),
                    (81, "Right"),
                    (82, "Right-Front Side"),
                    (83, "Right-Back Side"),
                    (98, "Not Reported"),
                    (99, "Damage Areas Unknown"),
                ],
                default=99,
            ),
        ),
    ]
