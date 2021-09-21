from django.contrib import admin
from django.urls import path, include

from homeapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('create', views.createPassword, name='create_password'),
    path('viewdetails/<int:id>', views.viewDetails, name='viewdetails'),
]
