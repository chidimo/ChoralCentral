from django.shortcuts import render

def google_webmaster_verify(request):
    template = "google364c8377c791cdf3.html"
    return render(request, template, {})

def credits(request):
    template = "credits.html"
    return render(request, template, {})

def coming_soon(request):
    template = "coming_soon.html"
    return render(request, template, {})

def terms_and_conditions(request):
    template = "terms_and_conditions.html"
    return render(request, template, {})

def privacy_policy(request):
    template = "privacy_policy.html"
    return render(request, template, {})

def api(request):
    template = "api.html"
    return render(request, template, {})

def api_docs(request):
    template = "api_docs.html"
    return render(request, template, {})


