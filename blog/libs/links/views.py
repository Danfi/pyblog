#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.libs.links.forms import linksForm
from blog.libs.links.models import links
from sysadmin.decorator import admin_required
from sysadmin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def addLink(request, template_name):
    if request.method == 'POST':
        form = linksForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('getlinklist'))
    else:
        form = linksForm()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('addlink'),
            'page_title':_('Add Link')
        }
    )
    return HttpResponse(vt.render(c))

@login_required
@admin_required
def editLink(request,tid,template_name):
    try:
        tlinks = links.objects.get(id=tid)
        if request.method == 'POST':
            form = linksForm(request.POST,instance=tlinks)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('getlinklist'))
        else:
            form = linksForm(instance=tlinks)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
            {
                'form':form,
                'form_url':reverse('editlink',args=[tid]),
                'page_title':_('Edit Link')
            }
        )
        return HttpResponse(vt.render(c))
    except links.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Link does not exist.')},
            context_instance=RequestContext(request)
        )

@login_required
@admin_required
def getLinkList(request, template_name):
    queryset=links.objects.all()
    search_fields = ['name','url']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'page_title':_('Link List'),
            'search_url':reverse('getlinklist'),
            'search_field':_('Name,Url')
        }
    )

@csrf_exempt
@login_required
@admin_required
def delLink(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            links.objects.filter(id__in=tids).delete()
    return HttpResponseRedirect(reverse('getlinklist'))