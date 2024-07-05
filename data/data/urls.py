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
from fatalities.views import crashes, favicon_view, nonmotorist_map, schema, accident_summary, map, leaflet, testmap, folium_map, post_comment
from .api import api
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("map", map, name="map"),
    path("folium_map", folium_map, name="folium_map"),
    path("", crashes, name="homepage"),
    path("schema", schema, name="schema"),
    path("leaflet", leaflet, name="leaflet"),
    path("testmap", testmap, name="testmap"),
    path("nonmotorist_map", nonmotorist_map, name="nonmotorist_map"),
    path("post_comment", post_comment, name="post_comment"),

    path("accidents/<int:id>/", accident_summary, name="accident_summary"),
    path("v1/", api.urls),
    re_path(r'^favicon\.ico$', favicon_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
