"""Custom template tags and filters"""
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def pluralize_my_words(word):
    pass

@register.filter()
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter()
def how_many_comments(comment_queryset, count=10):
    """Returns specified number of comments"""

    if count == "all":
        return comment_queryset
    return comment_queryset[:int(count)]