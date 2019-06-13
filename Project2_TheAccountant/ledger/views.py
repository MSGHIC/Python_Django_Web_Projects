from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Company, Payment, Account, Archive, Loan, ApproveLoan, Bills_update, UserQueries
from .forms import PaymentForm, ArchiveForm, LoanForm,  ApproveLoanForm, BillForm, FeedbackForm
from django.db import IntegrityError, transaction
import os
from django.http import FileResponse
import datetime
from datetime import date
from django.core.mail import send_mail, get_connection
from django.conf import settings

# Create your views here.
def index(request):
    """The home page for TheAccountant"""
    
    #give access to company data
    obj = Company.objects.get(id=1)
    
    context = { 
            'object':obj,
            }
    return render(request, 'ledger/index.html', context)


@login_required
@transaction.atomic
def payment(request):
    """record a payment and update necessary fields"""
    if request.method != 'POST':
       # No data submitted; create a blank form.
       form = PaymentForm()
    else:
        # POST data submitted; process data.
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment_amount = request.POST['payment_amount']
            payment_type = request.POST['payment_type']
            #receipt = request.FILES['receipt']
            paid_by = request.user 
             
            #relationships
            account = Account.objects.get(owner=request.user) 
            company = Company.objects.get(id=1)
            
             #update Company Database
                        
            try:
               with transaction.atomic(): 
                  
                    #update company finance data
                                                                                            
                    if payment_type == 'GT':
                       company.Company_value = company.Company_value +int(payment_amount) + company.Balance_BF
                       company.save()
                    elif payment_type == 'LP':
                        company.total_debts -= int(payment_amount)
                        account.member_loan -= int(payment_amount)
                        company.save()
                        account.save()  
                    elif payment_type == 'SP':
                        company.total_debts -= int(payment_amount)
                    
                        account.member_debt -= int(payment_amount)
                        company.save()
                        account.save()
                   
            except IntegrityError:
                   company.set_failed_flag()
            
         
          
            new_payment = Payment(payment_amount=payment_amount,
                                  payment_type=payment_type,
                                  paid_by=paid_by, #receipt =receipt ,  
                                  account=account, company=company)
            new_payment.save()
            
           #send mail to CA
            message =  request.POST['payment_type'] +' payment  '+  'amounting to  '+str(payment_amount)
            send_mail('TheAccountant-New payment recorded  ',
    		 message, 
    		 settings.EMAIL_HOST_USER,
    		 ['msgizaasum@gmail.com'], 
    		 fail_silently=True)
            
            #redirect to index page
            return HttpResponseRedirect(reverse('ledger:index'))
    
    #give access to company data
    obj = Company.objects.get(id=1)
                           
    #send the form to the template in the context dictionary
    context = {'form': form, 'object':obj}
    return render(request, 'ledger/payment.html', context)


@login_required
def company_finance(request):
    """update company finance details and render them to company_finance page"""
   #access all fileds in company object
    obj = Company.objects.get(id=1)
    
    #option one
    """context = {
            'Company_name': obj.Company_name,
            'Company_slogan': obj.Company_slogan,
            'Company_logo': obj.Company_logo,
            'Number_of_members':obj.Number_of_members,
            'Balance_BF':obj.Balance_BF,
            'total_debts':obj.total_debts,
            'Company_value':obj.Company_value,
            'general_share':obj.general_share ,
            'Liquid_value':obj. Liquid_value,
            } """
    #BEST OPTION
    context = {
            'object':obj, 'media_url':settings.MEDIA_URL
            }
  
    return render(request, 'ledger/company_finance.html', context)
 
    
@login_required   
def account_statement(request):
    """display member's account mini statement"""
   
    #access all fileds in company object and account
    obj = Company.objects.get(id=1)
    #retrieve updated account data
    obj_account = Account.objects.get(owner=request.user)
       
    obj_account.member_capital = obj.general_share - obj_account.member_debt
    obj_account.member_share = (obj_account.member_capital/(obj.Liquid_value+1))*100
 
    
    context = {
            'object1':obj_account, 'object':obj ,'media_url':settings.MEDIA_URL}
  
    return render(request, 'ledger/account_statement.html', context)


@login_required 
def archive(request):
    """post docs, also allow users to view docs"""
    if request.method != 'POST':
       # No data submitted; create a blank form.
       form = ArchiveForm()
    else:
        # POST data submitted; process data.
        form = ArchiveForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST['title']
            file = request.FILES['file']
            posted_by = request.user 
            
            new_post = Archive(title=title, file = file, posted_by =posted_by)
            new_post.save()
            
            #redirect to index page
            return HttpResponseRedirect(reverse('ledger:index'))
    
    #give access to company data
    obj = Company.objects.get(id=1)
                           
    #send the form to the template in the context dictionary
    context = {'form': form, 'object':obj}
    return render(request, 'ledger/archive.html', context)  
      

@login_required 
def archives(request):
    """display  docs in archive"""
    obj = Company.objects.get(id=1)
    archives = Archive.objects.order_by('date_added')
        
    context = {'archives': archives , 'object':obj}
    return render(request, 'ledger/archives.html', context)


@login_required 
def pdf_view(request):
    
    file_path = 'media/company_files/docs/Constitution.pdf' 
    try:
        return FileResponse(open(os.path.join(file_path), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404() 
        
@login_required 
def minutes_view(request):
   
   
    file_path = 'media/company_files/docs/minutes_18.pdf' 
    try:
        return FileResponse(open(os.path.join(file_path), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()    

      
@login_required 
@transaction.atomic
def loan_application(request):
    """capture loan application if user has no pending loan"""
    #compute loan terms
    account = Account.objects.get(owner=request.user)
    loan_code = account.pending_loan
   
    #give access to company data
    obj = Company.objects.get(id=1)
    
    if loan_code == 1:
        #when member submitted a loan application(Loan In-Review) 
        loan = Loan.objects.get(borrower=request.user,   status = 'In_Review')
        msg1 = 'Sorry, you need to clear a pending loan before you can apply for a new one.'
        msg2 = 'Thank you for understanding.'
        context = {'msg1':msg1,'msg2':msg2, 'loan':loan,'account':account, 'object':obj}
        return render(request, 'ledger/pending_loan.html', context)
    
    elif loan_code == 2: 
         #when member has an active loan (approved/rejected) 
         #if loan bal == 0; reset loan status to cleared 
         if account.member_loan == 0:
             account.pending_loan = 0
             account.save()
             #set loan status to cleared
             loan = Loan.objects.get(borrower=request.user,   status = 'AP')
             loan.status = 'CR'
             loan.save()
             
             return HttpResponseRedirect(reverse('ledger:loan_application'))
         else:
            loan = Loan.objects.get(borrower=request.user,   status = 'AP')
            msg1 = 'Sorry, you need to clear a pending loan before you can apply for a new one.'
            msg2 = 'Thank you for understanding.'
            context = {'msg1':msg1,'msg2':msg2, 'loan':loan,'account':account, 'object':obj}
            return render(request, 'ledger/pending_loan.html', context)
            
    else:
        money = account.member_capital-account.member_total_debts
        max_loan  = money*1.25-money*1.25%10000
		       
        if  max_loan < 100000:
            
            return HttpResponseRedirect(reverse('ledger:account_statement'))
           
 
        else:
        
            if request.method != 'POST':
               # No data submitted; create a blank form.
               
               form = LoanForm()
            else:
                # POST data submitted; process data.
              
                form = LoanForm(request.POST)
                if form.is_valid():
                    loan_amount = request.POST['loan_amount']
                    duration = request.POST['duration']
                    reason = request.POST['reason']
                    borrower = request.user 
                    
                    
                    if int(loan_amount) < 500001:
                        interest = int(loan_amount) * 0.05*int(duration)
                    elif int(loan_amount) < 1000001:
                          interest = int(loan_amount) * 0.04*int(duration)
                    elif int(loan_amount) < 3000001:
                          interest = int(loan_amount) * 0.03*int(duration)
                    else:
                        interest = int(loan_amount) * 0.02*int(duration)
               
                    account = Account.objects.get(owner=request.user)
                    try:
                        with transaction.atomic(): 
                            #record loan in account
                            account.pending_loan =  1
                        account.save() 
                    except IntegrityError:  
                           'None'
                              
                    new_loan = Loan(loan_amount=loan_amount,
                                           duration= duration,
                                           borrower= borrower, 
                                           maxLoan = max_loan,
                                           interest= interest,
                                           account = account,
                                           reason=reason,
                                           
                                          )
                    new_loan.save()
                              
                    #redirect to index page
                    return HttpResponseRedirect(reverse('ledger:loan_approval'))          
            
           
                                   
            #send the form to the template in the context dictionary
            context = {'form': form, 'object':obj, 'max_loan': max_loan}
            return render(request, 'ledger/loan_application.html', context)


@login_required 
def loan_approval(request):
    """feedback after loan application"""
    
    #give access to company data
    obj = Company.objects.get(id=1)
  
    obj_loan = Loan.objects.get(borrower=request.user, date_added=date.today()) 
    context = { 
            'object':obj, 'object2': obj_loan,
            }
    return render(request, 'ledger/loan_approval.html', context)


@login_required 
@transaction.atomic
def loan_approval_action(request):
    """feedback after loan application"""
    #approval = ApproveLoan()
    #approval.save()
    company = Company.objects.get(id=1)
    
    if request.method != 'POST':
        form =  ApproveLoanForm()
    else:
        # POST data submitted; process data.
        form = ApproveLoanForm(request.POST)
        #form = SubmissionQuickReplyForm(request.POST)
        if form.is_valid():
            #loan_application =  form.cleaned_data.get('choice')
            status = request.POST['status']
            loan_application = request.POST['loan_application']
            remarks = request.POST['remarks']
            decision =  status        
            
            #get loan owner
            loan =  Loan.objects.get(id=loan_application)
           
            user = loan.borrower
            account = Account.objects.get(owner=user)
          
            try:
                with transaction.atomic(): 
                    #update loan status for borrower
                   
                    loan.status = status
                loan.save()
            except IntegrityError:  
                       'None'
                       
            #IF LOAN IS APPROVED
            if status == 'AP':
                
                try:
                    with transaction.atomic():
                        #update user account
                        
                        account.member_loan +=(loan.loan_amount + loan.interest)
                        account.pending_loan = 2
                    account.save()
                except IntegrityError:  
                           'None'
                
               
                try:
                    with transaction.atomic():
                        #update company finance 
                        company.total_debts += (loan.loan_amount + loan.interest)
                        company.Company_value += loan.interest
                    company.save()
                except IntegrityError:  
                           'None'
                           
                company = Company.objects.get(id=1)
                try:
                    with transaction.atomic():
                        #update company finance 
                        company.general_share = company.Company_value / company.Number_of_members
                    company.save()
                    
                except IntegrityError:  
                           'None'
       
        
                new_approval = ApproveLoan(loan_application=loan_application, status=status, decision=decision, remarks = remarks ,account=account, company=company, loan=loan)
                new_approval.save()
                
                return HttpResponseRedirect(reverse('ledger:loan_approval_action'))
            
            #IF LOAN IS REJECTED
            elif status == 'RJ':
              
                account.pending_loan = 0
                account.save()
                
        
                new_approval = ApproveLoan(loan_application=loan_application, status=status, decision=decision, remarks = remarks ,account=account, company=company, loan=loan)
                new_approval.save()
                
                return HttpResponseRedirect(reverse('ledger:loan_approval_action'))
            
        new_approval = ApproveLoan(loan_application=loan_application, status=status, decision=decision, remarks = remarks ,account=account, company=company, loan=loan)
        new_approval.save()
                
        return HttpResponseRedirect(reverse('ledger:loan_approval_action'))
    
    context = { 
            'form': form, 'object': company, 
            }
    return render(request, 'ledger/loan_approval_action.html', context)


@login_required 
@transaction.atomic
def bill_increament(request):
    """increaments members debts by monthly subcription amount eg 100k"""
    company = Company.objects.get(id=1)
    
        
    # getting current date and time
    d = datetime.datetime.today()
    bills_day = 21
    monthly_bill = 100000
    
    if request.method != 'POST':
        
        if d.day != bills_day:
             if d.day < bills_day:
                  msg = 'Please come back on '+ str(bills_day)+' day of this month to bill members'
             else:
                 msg = 'Please come back on '+ str(bills_day) +' day of next month to bill members'
             
                     
             context = {'msg':msg,'object':company}
             return render(request, 'ledger/no_billing.html', context)
         
        else:
             form = BillForm()
             
    else:
                
         try:
             Bills_update.objects.get(action_date = date.today(), count = 1)
             if Bills_update:
                  msg = 'Already billed, please come back on '+ str(bills_day) +' day of next month to bill members'
                  context = {'msg':msg,'object':company}
                  return render(request, 'ledger/no_billing.html', context)
                 
         except Bills_update.DoesNotExist:
             """
             update = Bills_update(updated_by = request.user)
             update.save()
                 
             bill_update = Bills_update.objects.get(action_date = date.today(), count = 0)
             
             """  
             form = BillForm(request.POST)
             if form.is_valid():
                               
                 accounts = Account.objects.all()
                 for account in accounts:
                     account.member_debt += monthly_bill
                     account.save()
                     company.total_debts += monthly_bill
                     company.Company_value += monthly_bill
                     company.save()
                 count = 1
                     
                 
                 bill_update = Bills_update(count = count, updated_by =  request.user, bill_amount  = monthly_bill, action_date = date.today())
                     
                 bill_update.save()
                                     
                 return HttpResponseRedirect(reverse('ledger:index'))
              
               
    context = { 
            'object': company, 'form': form,  'amount': monthly_bill
            }
    return render(request, 'ledger/bill_increament.html', context)           
               
def feedback(request):
    submitted = False
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            assert True
            con = get_connection('django.core.mail.backends.console.EmailBackend')
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
                connection=con
            )
            new_query =  UserQueries(name=cd['name'], email=cd['email'],subject=cd['subject'],message=cd['message'])
            new_query.save()
            return HttpResponseRedirect('/feedback?submitted=True')
    else:
        form = FeedbackForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'ledger/feedback.html', {'form': form,  'submitted': submitted})
       
    