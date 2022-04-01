from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(value, search_term, autoescape=True):
    return mark_safe(value.replace(search_term, "<span class='highlight'>%s</span>" % search_term))