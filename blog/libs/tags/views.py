#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.libs.tags.forms import tagsForm
from blog.libs.tags.models import tags
from sysadmin.decorator import admin_required
from sysadmin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def addTag(request, template_name):
    if request.method == 'POST':
        form = tagsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('gettaglist'))
    else:
        form = tagsForm()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('addtag'),
            'page_title':_('Add Tag')
        }
    )
    return HttpResponse(vt.render(c))

@login_required
@admin_required
def editTag(request,tid,template_name):
    try:
        ttags = tags.objects.get(id=tid)
        if request.method == 'POST':
            form = tagsForm(request.POST,instance=ttags)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('gettaglist'))
        else:
            form = tagsForm(instance=ttags)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
            {
                'form':form,
                'form_url':reverse('edittag',args=[tid]),
                'page_title':_('Edit Tag')
            }
        )
        return HttpResponse(vt.render(c))
    except tags.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Tag does not exist.')},
            context_instance=RequestContext(request)
        )

@login_required
@admin_required
def getTagList(request, template_name):
    queryset=tags.objects.order_by('-actionLatest')
    search_fields = ['name']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'page_title':_('Tag List'),
            'search_url':reverse('gettaglist'),
            'search_field':_('Tag Name')
        }
    )

@csrf_exempt
@login_required
@admin_required
def delTag(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            tags.objects.filter(id__in=tids).delete()
    return HttpResponseRedirect(reverse('gettaglist'))