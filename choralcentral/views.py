from django.shortcuts import render

def google_webmaster_verify(request):
    template = "google364c8377c791cdf3.html"
    return render(request, template, {})

def credits(request):
    template = "credits.html"
    return render(request, template, {})