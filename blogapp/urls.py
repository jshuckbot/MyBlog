from django.urls import path

from blogapp import views
from blogapp.apps import BlogappConfig

app_name = BlogappConfig.name

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),
]
