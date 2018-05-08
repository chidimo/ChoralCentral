from django.shortcuts import redirect, reverse
from django.contrib import messages

def check_user_quota(func):
    """Checks whether a user has enough quota to make an API call"""
    def check_and_call(request, *args, **kwargs):
        siteuser = request.user.siteuser
        remaining_quota = siteuser.remaining_quota
        if remaining_quota > 0:
            siteuser.used += 1
            siteuser.save(update_fields=['used'])
            messages.warning(request, "Remaining quota: {}".format(siteuser.remaining_quota))
            return func(request, *args, **kwargs)
        messages.error(request, "You've exceeded your API quota")
        return redirect(reverse("siteuser:detail", kwargs={"pk" : siteuser.pk, "slug" : siteuser.slug}))
    return check_and_call