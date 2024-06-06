from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("", views.default),
    path("newpage/", views.new_page),
    path("newpage/<pageid>/", views.newpage),
    path("search-notion/", views.search_notion),
]
