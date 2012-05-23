#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from admin.utils import getBlogTheme
from django.utils.translation import ugettext_lazy as _

def error404(request):
    vt = loader.get_template('themes/'+getBlogTheme()+'/404.html')
    c = RequestContext(
        request,
            {
            'page_title':_('404 Error')
        }
    )
    return HttpResponse(vt.render(c))

def error500(request):
    vt = loader.get_template('themes/'+getBlogTheme()+'/500.html')
    c = RequestContext(
        request,
            {
            'page_title':_('500 Error')
        }
    )
    return HttpResponse(vt.render(c))