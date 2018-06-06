from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib import messages

def get_tempo_text(tempo):
    if not tempo:
        return "Not set"
    if tempo <= 25:
        return "Larghissimo"
    elif 40 <= tempo <= 45:
        return "Grave"
    elif 46 <= tempo <= 50:
        return "Largo"
    elif 51 <= tempo <= 60:
        return "Lento"
    elif 61 <= tempo <= 80:
        return "Andante"
    elif 81 <= tempo <= 100:
        return "Moderato"
    elif 101 <= tempo <= 125:
        return "Allegretto"
    elif 126 <= tempo <= 145:
        return "Vivace"
    elif 146 <= tempo <= 200:
        return "Presto"
    else:
        return "Prestissimo"

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
import os


try:
    from weasyprint import HTML
except:
    pass

MY_APPS = ("asset", "credit", "debit", "establishment", "personnel", "service")

def render_to_pdf(request, template, context):
    """Generate pdf table with weasyprint"""

    # render html with specified stylesheet
    css_path = os.path.join(settings.BASE_DIR + settings.STATIC_URL + 'css/reader_view.css')
    html = render_to_string(template, context)
    html = HTML(string=html, encoding='ISO-8859-1')
    pdf = html.write_pdf(stylesheets=[css_path])

    file_name_slug = slugify('ChoralCentral {}'.format(context['song'].title))
    content_disposition = 'inline; filename={}.pdf'.format(file_name_slug)

    # Return http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = content_disposition
    response['Content-Transfer-Encoding'] = 'binary'
    response.write(pdf)
    return response
