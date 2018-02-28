import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

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

    # Create http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = content_disposition
    response['Content-Transfer-Encoding'] = 'binary'
    response.write(pdf)
    return response

def get_tempo_text(tempo):
    if not tempo:
        return
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
