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
def count_published(queryset):
    """Return a count of songs with publish=True"""
    return queryset.filter(publish=True).count()
