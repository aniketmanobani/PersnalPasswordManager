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
    path('apps-passwords/', views.appsPassword, name='apps_password'),
    path('website-passwords/', views.websitePassword, name='website_password'),

    path('other-passwords/', views.otherPassword, name='other_password'),
    path('delete/<int:id>', views.deletePass, name='deletePass'),
    path('editpass/<int:id>', views.editpass, name='editpass'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),

]
