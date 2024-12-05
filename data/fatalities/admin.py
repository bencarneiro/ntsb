from django.contrib import admin
from fatalities.models import Comment, PodcastEpisode

# Register your models here.

@admin.register(Comment)
class AuthorAdmin(admin.ModelAdmin):
    fields = ["comment"]

@admin.register(PodcastEpisode)
class PodcastAdmin(admin.ModelAdmin):
    fields = ["title", "description", "audio_file", "slug"]