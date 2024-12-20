# Generated by Django 4.2.16 on 2024-12-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fatalities", "0028_fatalitytotals_bike_fatalities_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PodcastEpisode",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("audio_file", models.FileField(upload_to="podcasts/")),
                ("publish_date", models.DateTimeField(auto_now_add=True)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
    ]
