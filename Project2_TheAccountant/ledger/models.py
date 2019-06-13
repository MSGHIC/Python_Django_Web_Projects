from django.db import models
from datetime import date
from django.conf import settings
#from django.contrib.auth.models import User
# Create your models here.

User = settings.AUTH_USER_MODEL

import cloudinary
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Company(models.Model):
    """- computes and returns
       *current value of the company (Cv)
           - Cv = balance + sum of all debts
       *company's general share(Gs)
            -Gs = Cv/n ; n is no. of members"""
    Company_name = models.CharField(max_length=50, default='addCompanyName') 
    Company_slogan = models.CharField(max_length=50, default='addCompanySlogan')
    """
    Company_logo = models.ImageField(upload_to='company_files', default='media/company_files/no-image.jpg')
    #can work with dropbox setting
    """
    Number_of_members = models.PositiveSmallIntegerField(default = 4)
    Balance_BF =  models.PositiveIntegerField(default = 0)
    total_debts = models.PositiveIntegerField(default = 0)
    Company_value  = models.PositiveIntegerField(default = 0)
    general_share = models.PositiveIntegerField(default = 0)
    Liquid_value =  models.PositiveIntegerField(default = 0)
    
    ## Points to a Cloudinary image , needed for deploy
    Company_logo = CloudinaryField('image',  default='media/uploads/image.png')
    
    ## Points to a Cloudinary video
    site_video = CloudinaryField(resource_type='video', default='media/uploads/video.mp4')
  
    def save(self, *args, **kwargs):
        #self.Company_value = self.Balance_BF + self.total_debts
        self.general_share = self.Company_value / self.Number_of_members
        self.Liquid_value = self.Company_value - self.total_debts
        
        super(Company, self).save(*args, **kwargs)
           
    def __str__(self):
        """Return a string representation of the model."""
        return str(self.Company_name)

#delete an image from Cloudinary when it’s model instance is deleted in your app
@receiver(pre_delete, sender=Company)
def photo_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.Company_logo.public_id)  

#delete an image from Cloudinary when it’s model instance is deleted in your app
@receiver(pre_delete, sender=Company)
def video_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.site_video.public_id)
  

class Account(models.Model):
    """A member's account in the company"""   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    date_added = models.DateTimeField(auto_now_add=True)
    pending_loan =  models.IntegerField(default=0)
    member_debt = models.PositiveIntegerField(default = 0)
    member_capital = models.IntegerField(default = 0)
    member_share = models.IntegerField(default = 0)
    member_loan = models.PositiveIntegerField(default = 0)
    member_total_debts = models.PositiveIntegerField(default = 0)
    
   
    def save(self, *args, **kwargs):
        obj = Company.objects.get(id=1)
        self.member_capital = obj.general_share - self.member_debt
        self.member_share = (self.member_capital/(obj.Liquid_value+1))*100
        self.member_total_debts = self.member_loan + self.member_debt
               
        super(Account, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'accounts'
      
    def __str__(self):
        """return account owner"""
        return str(self.id)
    
    
class Payment(models.Model):
    """handles cash inflows and outflows"""
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    date_added = models.DateTimeField(auto_now_add=True)
    """
    receipt = models.ImageField(upload_to='receipts/%Y/%m/%d/')
    #can be used with dropbox setting
    """
    ## Points to a Cloudinary image , needed for deploy
    receipt = CloudinaryField('image',  default='media/uploads/image.png')
    transaction_id = models.AutoField(primary_key=True)
    
    LOAN_REPAYMENT = 'LP'
    GRANT = 'GT'
    SUBSCRIPTION = 'SP'
   
    
    Payment_Choices = (
            ( LOAN_REPAYMENT, 'Loan_repayment'),
            (GRANT, 'Grant'),
            (SUBSCRIPTION, 'Subscription'),
            
    )
    
    payment_type = models.CharField(
        max_length=20,
        choices=Payment_Choices,
        default = 'notSet',
    )
    
    payment_amount = models.PositiveIntegerField()
 
    def __str__(self):
        """Return a string representation of the model."""
        return str(self.transaction_id)

#delete an image from Cloudinary when it’s model instance is deleted in your app
@receiver(pre_delete, sender=Payment)
def receipt_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.receipt.public_id)    
        
class Archive(models.Model):
    """store documents """
    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    file  = models.FileField(upload_to = 'company_files/docs/') 
    date_added =  models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = 'archives'
      
    def __str__(self):
        """Return a string representation of the model."""
        return str(self.title)


from django.core.validators import MinValueValidator, MaxValueValidator
MIN = 1
MAX = 12
min_loan = 100000
max_loan = 7000000
    
class Loan(models.Model):
    """creates loan"""
   
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    maxLoan   = models.PositiveIntegerField(default=0)
    reason = models.TextField(max_length=255, default='State cause for borrowing and How you plan to pay back.') 
    date_added = models.DateTimeField()
    loan_amount = models.PositiveIntegerField(validators=[MinValueValidator(min_loan) , MaxValueValidator(max_loan)])
    duration = models.IntegerField(validators=[MinValueValidator(MIN), MaxValueValidator(MAX)])
    interest = models.PositiveIntegerField()
   
    monthly_installment =  models.PositiveIntegerField(default=0)
 
    status= models.CharField(max_length=20, default = 'In_Review')



    def save(self, *args, **kwargs):
        self.monthly_installment = (int(self.loan_amount) + int(self.interest))/int(self.duration)
        self.date_added = date.today()
        
        super(Loan, self).save(*args, **kwargs)
                      
    def __str__(self):
        """Return a string representation of the model."""
        return str(self.borrower)

    
class ApproveLoan(models.Model):
    """handle loan approval"""
    action_date =  models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    decision= models.CharField(max_length=20, default = 'In_Review')
    message = "Good luck with the loan, remember to be a responsible Borrower and pay in time....Chief Accountant"
    remarks= models.TextField(default = message)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    loan_application = models.CharField(max_length=50)
    
    
    In_Review = 'IR'
    Approved = 'AP'
    Rejected = 'RJ'
    Cleared = 'CR'
    
    
    status_Choices = (
           
            (In_Review, 'In-Review'),
             ( Approved, 'Approved'),
            (Rejected, 'Rejected'),
            (Cleared, 'Cleared'),
            )
    
    status= models.CharField(
        max_length=20,
        choices=status_Choices,
        default = 'select',
    )


 
    def __str__(self):
        """Return a string representation of the model."""
        return str(self.loan)
    
class Bills_update(models.Model):  
    """track bills updates"""
    action_date =  models.DateTimeField(auto_now_add=True)
    count =  models.PositiveIntegerField(default = 0)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_amount =  models.PositiveIntegerField(default=0)
          
    def __str__(self):
        """Return a string representation of the model."""
        return str(self. action_date)

class UserQueries(models.Model):  
    """store users' feedback"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
                       
    def __str__(self):
        """Return a string representation of the model."""
        return str(self. subject)
     