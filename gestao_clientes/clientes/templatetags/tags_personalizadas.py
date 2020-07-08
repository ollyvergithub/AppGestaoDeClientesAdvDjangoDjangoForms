from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def current_time(format_string):
    return datetime.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def tag_recebendo_contexto(context, format_string):
    return datetime.now().strftime(format_string)