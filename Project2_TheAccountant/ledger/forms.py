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
from .models import Payment, Archive, Loan, ApproveLoan, Bills_update,UserQueries
#auto build form to make payment
class PaymentForm(forms.ModelForm):
   
    class Meta:
        model = Payment
        #fields to include in the form.
        #payment_choice = forms.ChoiceField(choices = Payment.Payment_Choices, 
                                          # label="", initial='', widget=forms.Select(), required=True)
        fields = [ 'payment_type', 'payment_amount','receipt']
        # labels
        labels = {'receipt': 'Upload Receipt:', 'payment_type': 'Reason for payemnt(Select option):'
                  , 'payment_amount': 'Amount Paid:'}
    
#auto build form to make payment
class ArchiveForm(forms.ModelForm):
   
    class Meta:
        model = Archive
       
        fields = [ 'title', 'file']
        # labels
        labels = {'title': 'Document itle:', 'file': 'Upload File:'}
    

#Loan application form
class LoanForm(forms.ModelForm):
      class Meta:
          model = Loan
          
          fields = ['reason' ,'loan_amount', 'duration']
          
          # labels
          labels = {'reason':'Reason for borrowing:', 'loan_amount': 'How much do you need?', 'duration': 'In how many months to pay back?'}
          

#approve loan form         
class ApproveLoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApproveLoanForm, self).__init__(*args, **kwargs)
        self.fields['loan_application'] = forms.ModelChoiceField(
            #queryset=Loan.objects.filter(status="IR")#return only those in review
            #queryset=Loan.objects.all()#return only those in review
            queryset=Loan.objects.filter(status="In_Review")#return only those in review
        )

    class Meta:
        model = ApproveLoan
        fields = ['loan_application', 'remarks', 'status',]    
        labels = {'loan_application':'Application by:', 'remarks':'Remarks', 'status': 'Status:'}
        
class BillForm(forms.ModelForm):
    class Meta:
        model = Bills_update
        fields = []
    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = UserQueries
        fields = ['name','email', 'subject', 'message']
        labels = {'name':'Your Name','email':'Your e-mail address:','subject':'Subject:','message':'Message:'}
       
         
        
                       