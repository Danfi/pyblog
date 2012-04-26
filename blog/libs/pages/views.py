#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from blog.libs.pages.forms import pageForm
from blog.libs.articles.models import articles
from sysadmin.decorator import admin_required
from sysadmin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def addPage(request, template_name):
    act_type = 'publish'
    try:
        if request.GET['act_type']:
            act_type = request.GET['act_type']
    except MultiValueDictKeyError:
        pass
    if request.method == 'POST':
        form = pageForm(request.POST)
        if form.is_valid():
            t = form.save(request,act_type)
            if act_type == 'publish':
                return HttpResponseRedirect(reverse('getpagelist'))
            elif act_type == 'save':
                return HttpResponseRedirect(reverse('editpage',args=[t.id]))
    else:
        form = pageForm()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
            {
            'form':form,
            'page_title':reverse('addpage'),
            'form_title':_('Add Page'),
            }
    )
    return HttpResponse(vt.render(c))

@login_required
@admin_required
def editPage(request,tid,template_name):
    act_type = 'publish'
    try:
        if request.GET['act_type']:
            act_type = request.GET['act_type']
    except MultiValueDictKeyError:
        pass
    try:
        tarticles = articles.objects.get(id=tid)
        if request.method == 'POST':
            form = pageForm(request.POST,instance=tarticles)
            if form.is_valid():
                t = form.save(request,act_type)
                if act_type == 'publish':
                    return HttpResponseRedirect(reverse('getpagelist'))
                elif act_type == 'save':
                    return HttpResponseRedirect(reverse('editpage',args=[t.id]))
        else:
            form = pageForm(instance=tarticles)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
                {
                'form':form,
                'page_title':reverse('editpage',args=[tid]),
                'form_title':_('Edit Page'),
                }
        )
        return HttpResponse(vt.render(c))
    except articles.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Page does not exist.')},
            context_instance=RequestContext(request)
        )

@login_required
@admin_required
def getPageList(request, template_name):
    queryset=articles.objects.filter(type='page').order_by('-publishTime')
    search_fields = ['title']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'page_title':_('Page List'),
            'search_url':reverse('getpagelist'),
            'search_field':_('Title')
        }
    )
