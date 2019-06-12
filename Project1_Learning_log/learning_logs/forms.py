# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 21:07:13 2018

@author: MSG
"""

"""Any page that lets a user enter and submit information on a web page is a
form, even if it doesn’t look like one.

this forms.py will build forms for requested pages to 
allow users enter  information
"""
#import Django  forms module 
from django import forms
#import models to work with(model the form bases on)
from .models import Topic, Entry

#auto build form to add topics
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        #fields to include in the form.
        fields = ['text']
        #no label needed
        labels = {'text': ''}
    
#auto build form to add entries
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        #fields to include in the form.
        fields = ['text']
        #no label needed
        labels = {'text': ''}
        #A widget is an HTML form element,
        #such as a single-line text box, multi-line text area, or drop-down list
        #override Django’s default widget choices
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
        
        
#delete form
class DeleteForm(forms.ModelForm):
    class Meta:
        model = Topic
        #fields to include in the form.
        fields = ['text']
        #no label needed
        labels = {'text': ''}
    
        