from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("", views.home),
    # re_path(r'^items/(?P<ids>(\d+(_\d+)*))/$', views.getpage),
    path("<pageid>/", views.getpage),
    path("<pageid>/save/", views.savepage),
]
