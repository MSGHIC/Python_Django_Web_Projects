# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 23:28:04 2018

@author: MSG
"""

"""Defines URL patterns for learning_logs."""
"""from django.urls import path
from . import views

urlpatterns = [
    path(' ', views.index, name='index'),
]"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    # Show all topics.
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    #page url for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    #page url for adding  topic entries
    path('new_entry/<int:topic_id>', views.new_entry, name='new_entry'),
    # Page for editing an entry
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),
    # Page for editing an topic
    path('edit_topic/<int:topic_id>', views.edit_topic, name='edit_topic'),
    # Page for deleting a topic
    path('delete_topic/<int:topic_id>', views.delete_topic, name='delete_topic'),
    # Page for deleting an entry
    path('delete_entry/<int:entry_id>', views.delete_entry, name='delete_entry'),
    
]