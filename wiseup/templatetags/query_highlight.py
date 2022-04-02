from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(value, search_term, autoescape=True):
    # first compile the regex pattern using the search_term
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)

    # now replace
    new_value = pattern.sub('<span class="highlight">\g<0></span>', value)
    return mark_safe(new_value)
    # return mark_safe(value.replace(search_term, "<span class='highlight'>%s</span>" % search_term))