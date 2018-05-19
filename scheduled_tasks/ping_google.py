from django.contrib.sitemaps import ping_google

try:
    ping_google()
except Exception:
    print("Google cannot be found.")
    pass