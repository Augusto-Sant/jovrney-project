from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms
from django.views.generic import TemplateView
from . import models
# Create your views here.

### PROFILE
class ProfileView(TemplateView):
    """Profile template view"""
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['profile'] = get_object_or_404(models.UserProfile.objects.filter(pk=self.request.user.pk))
            return context



### Registering
def register_view(request):
    """returns view of login form"""
    if request.user.is_authenticated:
        return HttpResponse("Registered already")
    else:
        registered = False
        form = forms.User_form()
        if request.method == 'POST':
            form = forms.User_form(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()
                registered = True
        else:
            # Was not an HTTP post so we just render the forms as blank.
            form = forms.User_form()

        return render(request,"register_form.html",{'form':form,'registered':registered,})

def user_login(request):
    """User login, gets username and password and authenticates."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # Log the user in.
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        #Nothing has been provided for username or password.
        return render(request, "login.html", {})

@login_required #REQUIRES LOGIN TO SEE
def user_logout(request):
    """User logout."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))