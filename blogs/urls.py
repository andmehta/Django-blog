"""
URL configuration for blogs project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blogposts/", include("blogposts.urls")),
]
