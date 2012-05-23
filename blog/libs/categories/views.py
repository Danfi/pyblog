#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.libs.categories.forms import categoriesForm
from blog.libs.categories.models import categories
from admin.decorator import admin_required
from admin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def addCategory(request, template_name):
    if request.method == 'POST':
        form = categoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('getcategorylist'))
    else:
        form = categoriesForm()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('addcategory'),
            'page_title':_('Add Category')
        }
    )
    return HttpResponse(vt.render(c))

@login_required
@admin_required
def editCategory(request,tid,template_name):
    try:
        tcategories = categories.objects.get(id=tid)
        if request.method == 'POST':
            form = categoriesForm(request.POST,instance=tcategories)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('getcategorylist'))
        else:
            form = categoriesForm(instance=tcategories)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
            {
                'form':form,
                'form_url':reverse('editcategory',args=[tid]),
                'page_title':_('Edit Category')
            }
        )
        return HttpResponse(vt.render(c))
    except categories.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Category does not exist.')},
            context_instance=RequestContext(request)
        )

@login_required
@admin_required
def getCategoryList(request, template_name):
    queryset=categories.objects.all()
    search_fields = ['name','url']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'page_title':_('Category List'),
            'search_url':reverse('getcategorylist'),
            'search_field':_('Category Name')
        }
    )

@csrf_exempt
@login_required
@admin_required
def delCategory(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            categories.objects.filter(id__in=tids).delete()
    return HttpResponseRedirect(reverse('getcategorylist'))