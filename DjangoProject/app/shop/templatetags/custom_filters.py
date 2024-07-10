from django import template

register = template.Library()

@register.filter
def to_0(value):
    return range(value, 0, -1)