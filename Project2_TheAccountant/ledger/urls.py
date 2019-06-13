# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 17:26:14 2018

@author: MSG
"""

from django.urls import path

from . import views

app_name = 'ledger'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'), 
    #make_payment
    path('payment/', views.payment, name='payment'), 
    #view company financial report
    path('company_finance', views.company_finance, name='company_finance'),
    #view account_statement
    path('account_statement', views.account_statement, name='account_statement'),
    #archive
    path('archive/', views.archive, name='archive'), 
    #archives
    path('archives/', views.archives, name='archives'),
    #process_loan
    path('loan_application/', views.loan_application, name='loan_application'),
    #loan_approval_action
    path('loan_approval_action/', views.loan_approval_action, name='loan_approval_action'),
    #archives
    path('loan_approval/', views.loan_approval, name='loan_approval'),
    #view_pdf
    path('pdf_view/', views.pdf_view, name='pdf_view'),
    #view_minutes
    path('minutes_view/', views.minutes_view, name='minutes_view'),
    #update monthly bills
    path('bill_increament/', views.bill_increament, name='bill_increament'),
    path('feedback', views.feedback, name='feedback'),

      
]