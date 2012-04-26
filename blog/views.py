#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator

from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _
from blog.libs.articles.models import articles
from sysadmin.libs.settings.models import blogSettings

def homePage(request, template_name):
    tblogSettings = blogSettings.objects.get(id=1)
    queryset = articles.objects.filter(type='article',status='Published').order_by('-publishTime')
    page_result = Paginator(queryset, tblogSettings.articlesPerPage)
    page_range = page_result.page_range
    try:
        page = int(request.GET.get('page', '1'))
        if page not in page_range:
            page = 1
    except ValueError:
        page = 1
    t_page = page_result.page(page)
    object_result = t_page.object_list
    if t_page.has_previous():
        prev_page = page - 1
    else:
        prev_page = 0
    if t_page.has_next():
        next_page = page + 1
    else:
        next_page = 0
    context = {
        'prev_page': prev_page,
        'next_page': next_page,
        'object_result': object_result,
        'ishome':True
    }
    vt = loader.get_template(template_name)
    return HttpResponse(vt.render(RequestContext(request, context)))