from django.shortcuts import render

"""
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
"""  

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from ledger.models import Company

# Create your views here.
def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = CustomUserCreationForm()
    else:
        # Process completed form.
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            
            #send welcome mail
            #email(request)
            
            return HttpResponseRedirect(reverse('ledger:index'))

    #give access to company data
    obj = Company.objects.get(id=1)
    
    context = {'form': form, 'object':obj}
    return render(request, 'users/register.html', context)