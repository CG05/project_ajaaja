from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("", views.default),
    path("tab1/", views.tab1),
    path("tab3/", views.tab3),
]
