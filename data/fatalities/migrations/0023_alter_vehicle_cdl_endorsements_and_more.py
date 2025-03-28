# Generated by Django 4.1.5 on 2024-07-06 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0022_alter_damage_area_of_impact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="cdl_endorsements",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No Endorsements Required for This Vehicle"),
                    (1, "Endorsements Required, Complied With"),
                    (2, "Endorsements Required, Not Complied With"),
                    (3, "Endorsements Required, Compliance Unknown"),
                    (7, "No Driver Present/Unknown if Driver Present"),
                    (8, "Not Reported "),
                    (9, "Unknown, if Required"),
                ],
                default=0,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="cdl_license_status",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No Commercial Driver's License (CDL)"),
                    (1, "Suspended"),
                    (2, "Revoked"),
                    (3, "Expired"),
                    (4, "Cancelled or Denied"),
                    (5, "Disqualified"),
                    (6, "Valid"),
                    (7, "Commercial Learner's Permit (CLP)"),
                    (8, "Other - Not Valid"),
                    (97, "No Driver Present/Unknown if Driver Present"),
                    (98, "Not Reported"),
                    (99, "Unknown License Status"),
                ],
                default=99,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="compliance_with_license_restrictions",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No Restrictions or Not Applicable"),
                    (1, "Restrictions Complied With"),
                    (2, "Restrictions Not Complied With"),
                    (3, "Restrictions, Compliance Unknown"),
                    (7, "No Driver Present/Unknown if Driver Present"),
                    (8, "Not Reported"),
                    (9, "Unknown"),
                ],
                default=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="drivers_license_state",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No Driver Present (Since 2010)"),
                    (1, "Alabama"),
                    (2, "Alaska"),
                    (3, "American Samoa"),
                    (4, "Arizona"),
                    (5, "Arkansas"),
                    (6, "California"),
                    (8, "Colorado"),
                    (9, "Connecticut"),
                    (10, "Delaware"),
                    (11, "District of Columbia"),
                    (12, "Florida"),
                    (13, "Georgia"),
                    (14, "Guam"),
                    (15, "Hawaii"),
                    (16, "Idaho"),
                    (17, "Illinois"),
                    (18, "Indiana"),
                    (19, "Iowa"),
                    (20, "Kansas"),
                    (21, "Kentucky"),
                    (22, "Louisiana"),
                    (23, "Maine"),
                    (24, "Maryland"),
                    (25, "Massachusetts"),
                    (26, "Michigan"),
                    (27, "Minnesota"),
                    (28, "Mississippi"),
                    (29, "Missouri"),
                    (30, "Montana"),
                    (31, "Nebraska"),
                    (32, "Nevada"),
                    (33, "New Hampshire"),
                    (34, "New Jersey"),
                    (35, "New Mexico"),
                    (36, "New York"),
                    (37, "North Carolina"),
                    (38, "North Dakota"),
                    (39, "Ohio "),
                    (40, "Oklahoma"),
                    (41, "Oregon"),
                    (42, "Pennsylvania"),
                    (43, "Puerto Rico"),
                    (44, "Rhode Island"),
                    (45, "South Carolina"),
                    (46, "South Dakota"),
                    (47, "Tennessee"),
                    (48, "Texas"),
                    (49, "Utah"),
                    (50, "Vermont"),
                    (51, "Virginia"),
                    (52, "Virgin Islands"),
                    (53, "Washington"),
                    (54, "West Virginia"),
                    (55, "Wisconsin"),
                    (56, "Wyoming"),
                    (57, "Other U.S. Driver's License (Since 2018)"),
                    (93, "Indian Nation (Since 2009)"),
                    (94, "U.S. Government"),
                    (95, "Canada"),
                    (96, "Mexico"),
                    (97, "Other Foreign Country"),
                    (98, "Not Reported"),
                    (99, "Reported as Unknown"),
                ],
                default=98,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="license_compliance_with_class_of_vehicle",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "Not Licensed"),
                    (1, "No License Required for This Class Vehicle"),
                    (2, "No Valid License for This Class Vehicle"),
                    (3, "Valid License for This Class Vehicle"),
                    (6, "No Driver Present/Unknown if Driver Present"),
                    (7, "Not Reported "),
                    (
                        8,
                        "Unknown if CDL and/or CDL Endorsement Required for This Vehicle",
                    ),
                    (9, "Unknown"),
                ],
                default=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="month_of_newest_violation",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No Record"),
                    (1, "January"),
                    (2, "February"),
                    (3, "March"),
                    (4, "April"),
                    (5, "May"),
                    (6, "June"),
                    (7, "July"),
                    (8, "August"),
                    (9, "September"),
                    (10, "October"),
                    (11, "November"),
                    (12, "December"),
                    (98, "No Driver Present/Unknown if Driver Present"),
                    (99, "Unknown"),
                ],
                default=99,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="month_of_oldest_violation",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No Record"),
                    (1, "January"),
                    (2, "February"),
                    (3, "March"),
                    (4, "April"),
                    (5, "May"),
                    (6, "June"),
                    (7, "July"),
                    (8, "August"),
                    (9, "September"),
                    (10, "October"),
                    (11, "November"),
                    (12, "December"),
                    (98, "No Driver Present/Unknown if Driver Present"),
                    (99, "Unknown"),
                ],
                default=99,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="non_cdl_license_status",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "Not Licensed"),
                    (1, "Suspended"),
                    (2, "Revoked"),
                    (3, "Expired"),
                    (4, "Cancelled or Denied"),
                    (5, "Single-Class License"),
                    (6, "Valid"),
                    (7, "No Driver Present/Unknown if Driver"),
                    (9, "Unknown License Status"),
                ],
                default=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="non_cdl_license_type",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "Not Licensed"),
                    (1, "Full Driver License"),
                    (2, "Intermediate Driver License"),
                    (6, "No Driver Present/Unknown if Driver Present"),
                    (7, "Learner's Permit"),
                    (8, "Temporary License"),
                    (9, "Unknown License Type"),
                ],
                default=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="speeding_related",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (0, "No"),
                    (1, "Yes"),
                    (2, "Yes, Racing"),
                    (3, "Yes, Exceeded Speed Limit"),
                    (4, "Yes, Too Fast for Conditions"),
                    (5, "Yes, Specifics Unknown"),
                    (8, "No Driver Present/Unknown if Driver Present"),
                    (9, "Reported as Unknown"),
                ],
                default=9,
                null=True,
            ),
        ),
    ]
