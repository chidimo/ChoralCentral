from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

def star_or_unstar_object(siteuser, pk, app_label, model):
    """
    Generic function for starring objects

    Parameters
    ------------
    app_label : str
        Sent with ajax request
    model_name : str
        Sent with ajax request
    """
    # Get the object
    obj_ct = ContentType.objects.get(app_label=app_label, model=model)
    model_instance = obj_ct.get_object_for_this_type(pk=pk)

    if model_instance.likes.filter(screen_name=siteuser.screen_name).exists():
        model_instance.likes.remove(siteuser)
        data = {'success' : True, 'message' : 'You disliked this {}'.format(model)}
    else:
        model_instance.likes.add(siteuser)
        data = {'success' : True, 'message' : 'You liked this {}'.format(model)}

    like_count = model_instance.likes.count()
    model_instance.save(update_fields=['like_count'])
    return data

def get_tempo_text(tempo):
    if not tempo:
        return "Not set"
    if tempo <= 25:
        return "larghissimo"
    elif 40 <= tempo <= 45:
        return "grave"
    elif 46 <= tempo <= 50:
        return "largo"
    elif 51 <= tempo <= 60:
        return "lento"
    elif 61 <= tempo <= 80:
        return "andante"
    elif 81 <= tempo <= 100:
        return "moderato"
    elif 101 <= tempo <= 125:
        return "allegretto"
    elif 126 <= tempo <= 145:
        return "vivace"
    elif 146 <= tempo <= 200:
        return "presto"
    else:
        return "prestissimo"

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
