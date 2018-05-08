"""Custom template tags and filters"""

import os
import markdown
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def markdown_format(text):
    text = text.replace("\n", "<br>")
    text = text.replace("\n\n", "<br><br>")
    return mark_safe(markdown.markdown(text))

@register.filter()
def join_with_links(list_items, ):
    pass

@register.filter()
def published_author_songs(author_songs_queryset):
	"""Return all songs by author with status 'PUBLISHED'"""
	return author_songs_queryset.filter(status="PUBLISHED")

@register.filter()
def api_data_structures(somestring):
    """Properly format the data structure of API documentation view"""
    md = os.path.join(settings.BASE_DIR, 'templates', 'structures.md')
    with open(md, 'r+') as fh:
        s = fh.read()
    safe_html = mark_safe(markdown.markdown(s))
    return safe_html
