# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 12:38:14 2018

@author: MSG
"""

from django.urls import path
#importing a set of views 
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    # Login page.
    path('login/',
    	auth_views.LoginView.as_view(template_name='users/login.html'),
    	name='login'),
    # Logout page.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Registration page
    path('register/', views.register, name='register'),
]