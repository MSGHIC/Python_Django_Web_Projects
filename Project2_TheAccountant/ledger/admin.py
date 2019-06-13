from django.contrib import admin


# Register your models here.
from ledger.models import Company, Payment, Account, Archive, Loan, ApproveLoan, Bills_update,UserQueries
admin.site.register(Company)
admin.site.register(Payment)
admin.site.register(Account)
admin.site.register(Archive)
admin.site.register(Loan)
admin.site.register(ApproveLoan)
admin.site.register(Bills_update)
admin.site.register(UserQueries)

#customize admin header
admin.site.site_header = 'TheAccountant-Admin Panel'