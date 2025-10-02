from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Divise une chaîne selon un délimiteur"""
    return value.split(arg)

@register.filter
def mul(value, arg):
    """Multiplie deux valeurs"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """Soustrait deux valeurs"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Additionne deux valeurs"""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return 0
