# -*- coding: utf-8 -*-

from django import template
register = template.Library()

@register.filter
def truncatechars(s, num):
    """
    Truncates a string number of chars
    """
    length = int(num)
    if len(s) > length:
        return s[:length]+'&hellip;'
    else:
        return s
