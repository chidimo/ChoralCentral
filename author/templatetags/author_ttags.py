"""Custom template tags and filters"""
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def markdown_format(text):
    text = text.replace("\n", "<br>")
    text = text.replace("\n\n", "<br><br>")
    return mark_safe(markdown.markdown(text))

@register.filter()
def published_author_songs(author_songs_queryset):
	"""Return all songs by author with status 'PUBLISHED'"""
	return author_songs_queryset.filter(publish=True)