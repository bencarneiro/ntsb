"""data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from fatalities.views import PodcastFeed, crashes, favicon_view, texas, pedestrian_safety, privacy, beta, total_csv, vehicle_csv, nonmotorist_csv, nonmotorist, vehicle, new_map, nonmotorist_map, schema, accident_summary, map, leaflet, testmap, folium_map, post_comment, county_dashboard, total_fatalities, county_selector, county_table, info, comments, episode_detail, episodes
from .api import api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("map", new_map, name="map"),
    path("folium_map", folium_map, name="folium_map"),
    path("", crashes, name="homepage"),
    path("schema", schema, name="schema"),
    path("leaflet", leaflet, name="leaflet"),
    path("testmap", testmap, name="testmap"),
    path("nonmotorist_map", nonmotorist_map, name="nonmotorist_map"),
    path("post_comment", post_comment, name="post_comment"),
    path("county_selector", county_selector, name="county_selector"),
    path("county_table", county_table, name="county_table"),
    path("county_dashboard/<int:county_id>", county_dashboard, name="county_dashboard"),
    path("accidents/<int:id>/", accident_summary, name="accident_summary"),
    path("total_fatalities", total_fatalities, name="total_fatalities"),
    # path("new_map", new_map, name="new_map"),
    path("info", info, name="info"),
    path("total_csv", total_csv, name="total_csv"),
    path("vehicle_csv", vehicle_csv, name="vehicle_csv"),
    path("nonmotorist_csv", nonmotorist_csv, name="nonmotorist_csv"),
    path("nonmotorist", nonmotorist, name="nonmotorist"),
    path("vehicle", vehicle, name="vehicle"),
    path("beta", beta, name="beta"),
    path("pedestrian_safety", pedestrian_safety, name="pedestrian_safety"),
    path("v1/", api.urls),
    path("comments", comments, name="comments"),
    path('podcast/feed.xml', PodcastFeed(), name='podcast_feed'),  # RSS feed for podcast,
    path("podcast", episodes, name="episodes"),
    path("privacy", privacy, name="privacy"),
    path("episode_detail/<str:slug>/", episode_detail, name="episode_detail"),
    path("texas", texas, name="texas"),
    re_path(r'^favicon\.ico$', favicon_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

