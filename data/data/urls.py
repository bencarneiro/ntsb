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
from fatalities.views import PodcastFeed, new_mexico_csv, colorado_csv, contact, visionzeroblog, denver, denver_csv, state_blog, blog, sitemap, accident_list, get_counties_by_state, collect_email, gooner_army, visionzero, reddit, beta_redirect, favicon_view, texas, missed_connections, create_missed_connection, someone_died_here, connection, population, population_nonmotorist, pedestrian_safety, privacy, beta, total_csv, vehicle_csv, nonmotorist_csv, nonmotorist, vehicle, new_map, nonmotorist_map, schema, accident_summary, map, leaflet, testmap, folium_map, post_comment, post_missed_connection_comment, county_dashboard, total_fatalities, county_selector, county_table, info, comments, episode_detail, episodes, api_tutorial_notebook
from .api import api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("map", new_map, name="map"),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("folium_map", folium_map, name="folium_map"),
    path("", beta, name="homepage"),
    path("schema", schema, name="schema"),
    path("leaflet", leaflet, name="leaflet"),
    path("testmap", testmap, name="testmap"),
    path("contact", contact, name="contact"),
    path("nonmotorist_map", nonmotorist_map, name="nonmotorist_map"),
    path("post_comment", post_comment, name="post_comment"),
    path('accidents/', accident_list, name='accident_list'),
    path('accidents/counties/', get_counties_by_state, name='get_counties_by_state'),
    path("post_missed_connection_comment", post_missed_connection_comment, name="post_missed_connection_comment"),
    path("collect_email", collect_email, name="collect_email"),
    path("county_selector", county_selector, name="county_selector"),
    path("county_table", county_table, name="county_table"),
    path("county_dashboard/<int:county_id>", county_dashboard, name="county_dashboard"),
    path("accidents/<int:id>/", accident_summary, name="accident_summary"),
    path("crash/<int:id>/", accident_summary, name="crash_summary"),
    path("total_fatalities", total_fatalities, name="total_fatalities"),
    path("info", info, name="info"),
    path("total_csv", total_csv, name="total_csv"),
    path("denver_csv", denver_csv, name="denver_csv"),
    path("new_mexico_csv", new_mexico_csv, name="new_mexico_csv"),
    path("colorado_csv", colorado_csv, name="colorado_csv"),
    path("vehicle_csv", vehicle_csv, name="vehicle_csv"),
    path("nonmotorist_csv", nonmotorist_csv, name="nonmotorist_csv"),
    path("nonmotorist", nonmotorist, name="nonmotorist"),
    path("vehicle", vehicle, name="vehicle"),
    path("visionzero", visionzero, name="visionzero"),
    path("vision-zero-map", visionzeroblog, name="visionzeroblog"),
    path("beta", beta_redirect, name="beta"),
    path("pedestrian_safety", pedestrian_safety, name="pedestrian_safety"),
    path("v1/", api.urls),
    path("comments", comments, name="comments"),
    path('podcast/feed.xml', PodcastFeed(), name='podcast_feed'),  # RSS feed for podcast,
    path("podcast", episodes, name="episodes"),
    path("privacy", privacy, name="privacy"),
    path("episode_detail/<str:slug>/", episode_detail, name="episode_detail"),
    path("blog/<str:state>/", state_blog, name="state_blog"),
    path("texas", texas, name="texas"),
    path("denver", denver, name="denver"),
    path("population", population, name="population"),
    path("population_nonmotorist", population_nonmotorist, name="population_nonmotorist"),
    path("reddit", reddit, name="reddit"),
    path("goonarmy", gooner_army, name="goonarmy"),
    path("goonerarmy", gooner_army, name="goonerarmy"),
    path("goon-army", gooner_army, name="goon-army"),
    path("gooner-army", gooner_army, name="gooner-army"),
    path("goon_army", gooner_army, name="goon_army"),
    path("gooner_army", gooner_army, name="gooner_army"),
    path("missed_connections", missed_connections, name="missed_connections"),
    path("connection/<int:id>/", connection, name="connection"),
    path("create_missed_connection", create_missed_connection, name="create_missed_connection"),
    path("someone_died_here", someone_died_here, name="someone_died_here"),
    path("api_tutorial_notebook", api_tutorial_notebook, name="api_tutorial_notebook"),
    path("blog", blog, name="blog"),
    re_path(r'^favicon\.ico$', favicon_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

