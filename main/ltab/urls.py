from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("", views.default),
    path("newpage/<pageid>/", views.newpage),
    
]
