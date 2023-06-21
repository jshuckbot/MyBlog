from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from blogapp.sitemaps import PostSitemap

sitemaps = {"posts": PostSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blogapp/", include("blogapp.urls", namespace="blogapp")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]
