# Generated by Django 4.1.5 on 2024-06-15 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0013_alter_person_airbag_deployed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crashrelatedfactors",
            name="crash_related_factor",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (0, "None Noted"),
                    (
                        1,
                        "Inadequate Warning of Exits, Lanes Narrowing, Traffic Controls, etc.",
                    ),
                    (2, "Shoulder Design or Condition"),
                    (3, "Other Maintenance or Construction-Created Condition"),
                    (4, "No or Obscured Pavement Marking"),
                    (5, "Surface Under Water"),
                    (
                        6,
                        "Inadequate Construction or Poor Design of Roadway, Bridge, etc.",
                    ),
                    (7, "Surface Washed out (Caved in, Road Slippage)"),
                    (10, "Emergency Vehicle Related"),
                    (12, "Distracted Driver of a Non-Contact Vehicle"),
                    (13, "Aggressive Driving/Road Rage by Non-Contact Vehicle Driver"),
                    (
                        14,
                        "Motor Vehicle Struck by Falling Cargo or Something That Came Loose From or Something That Was Set in Motion by a Vehicle",
                    ),
                    (
                        15,
                        "Non-Occupant Struck by Falling Cargo, or Something Came Loose From or Something That Was Set in Motion by a Vehicle",
                    ),
                    (16, "Non-Occupant Struck Vehicle"),
                    (17, "Stopped Vehicle Set in Motion by Non-Driver"),
                    (
                        18,
                        "Date of Crash and Date of EMS Notification Were Not Same Day",
                    ),
                    (19, "Recent Previous Crash Scene Nearby"),
                    (20, "Police-Pursuit-Involved"),
                    (21, "Within Designated School Zone"),
                    (
                        22,
                        "Speed Limit Is a Statutory Limit as Recorded or Was Determined as This State’s “Basic Rule”",
                    ),
                    (23, "Indication of a Stalled/Disabled Vehicle"),
                    (
                        24,
                        "Unstabilized Situation Began and All Harmful Events Occurred off of the Roadway",
                    ),
                    (25, "Toll Booth/Plaza Related"),
                    (26, "Prior Non-Recurring Incident"),
                    (27, "Backup Due to Prior Crash"),
                    (28, "Regular Congestion"),
                    (30, "Obstructed Crosswalks"),
                    (31, "Related to a Bus Stop"),
                    (42, "Uncontrolled Intersection or Railroad Crossing"),
                    (99, "Unknown"),
                ],
                default=0,
            ),
        ),
    ]