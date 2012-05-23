#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
register = template.Library()

@register.inclusion_tag('listFilter.html')
def get_list_filter(title,turl,tfilter_name,tchoice):
    return {
        'title': _(title),
        'turl': reverse(turl),
        'tfilter_name': tfilter_name,
        'tchoice': tchoice
    }