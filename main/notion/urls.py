from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('guest/<user>/<pageNum>/', views.guest),
    path('save/<notionId>/', views.save),
    path('saveBody/<notionId>/', views.saveBody),
    path('saveCover/<notionId>/', views.saveCover, name='upload_cover'),
    path('sendEmail/', views.sendEmail, name='email'),
    path('remove/<notionId>/', views.remove),
    path("", views.index),
    path("createNewPage/", views.createNewPage),
    path('createChild/<notionId>/<url>/', views.createChild),
    path('<pageNum>/', views.pageNum),
]