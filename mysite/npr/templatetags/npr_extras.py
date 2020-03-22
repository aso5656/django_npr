from django import template
from django.utils.safestring import mark_safe
from re import IGNORECASE, compile, escape as rescape

register = template.Library()

#custom filter highlight search word

@register.filter(name='highlight')

def highlight(text,search):
    rgx = compile(rescape(search), IGNORECASE)
    #highlight search content, ignoring case
    return mark_safe(
        rgx.sub(
            lambda m: '<b class="text bg-warning">{}</b>'.format(m.group()),
            text
        )
    )