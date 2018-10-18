from django.shortcuts import render, redirect
from django.urls import reverse

from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from siteuser.models import SiteUser
from siteuser.forms import EmailAndPassWordGetterForm

CustomUser = get_user_model()

def home(request):
    template = 'home.html'
    form = EmailAndPassWordGetterForm()

    if request.user.is_authenticated:
        return redirect(reverse('song:song_index'))

    if request.method == 'POST':
        form = EmailAndPassWordGetterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend',)
            return redirect(reverse('song:song_index'))
        else:
            return render(request, template, {'form' : form})
    return render(request, template, {'form' : form})


def help_page(request):
    template = "help_page.html"
    return render(request, template, {})

def coming_soon(request):
    template = "coming_soon.html"
    return render(request, template, {})

def terms_of_use(request):
    template = "terms_of_use.html"
    return render(request, template, {})

def privacy_policy(request):
    template = "privacy_policy.html"
    return render(request, template, {})

def api(request):
    template = "api.html"
    return render(request, template, {})

def contact(request):
    template = "contact.html"
    return render(request, template, {})
