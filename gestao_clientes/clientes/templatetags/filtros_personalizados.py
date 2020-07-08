from django import template

register = template.Library()

@register.filter
def retorna_texto(data):
    return data + " - " + "Retornado por clientes-templatetags-filters.py - def retorna_texto"


@register.filter
def arredonda(valor, casas_decimais):
    return round(valor, casas_decimais)
