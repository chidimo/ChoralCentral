from django.shortcuts import render

def google_webmaster_verify(request):
    template = "google364c8377c791cdf3.html"
    return render(request, template, {})

def credits(request):
    template = "credits.html"
    return render(request, template, {})

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

def to_fix(request):
    template = "to_fix.html"
    return render(request, template, {})
