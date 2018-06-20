from django.shortcuts import render

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
