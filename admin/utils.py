#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.template.context import RequestContext
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_protect
from blog.libs.categories.models import categories
from admin.libs.settings.models import blogSettings
import os

def dictFormError(error=None):
    return dict((key, str(value)) for key, value in error.items())

def getBlogTheme():
    tblogSettings = blogSettings.objects.get(id=1)
    return '%s' %tblogSettings.theme

@csrf_protect
def get_datatables_records(request, queryset,search_fields,template_name,extra_context={}):
    if queryset:
        if request.method == 'POST':
            if search_fields:
                outputQ = None
                for t_field in search_fields:
                    kwargz = {t_field + "__icontains": request.POST['search']}
                    outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
                queryset = queryset.filter(outputQ).distinct()
        else:
            try:
                if request.GET['t_filter']:
                    t_filter_value = request.GET['t_filter_value']
                    if t_filter_value == 'true':
                        t_filter_value = True
                    elif t_filter_value == 'false':
                        t_filter_value = False
                    kwargz = {request.GET['t_filter_name']: t_filter_value}
                    queryset = queryset.filter(Q(**kwargz)).distinct()
            except MultiValueDictKeyError:
                pass
        page_result = Paginator(queryset, 12)
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
        }
    else:
        context = {
            'object_result': None,
            }
    context.update(extra_context)
    vt = loader.get_template(template_name)
    return HttpResponse(vt.render(RequestContext(request, context)))

def sortCategory():
    tcs=[('','------')]
    t_no_parent = categories.objects.filter(parent=None).order_by('id')
    if t_no_parent:
        for tnp in t_no_parent:
            tcs.append((tnp.id,tnp.name))
            tcs = getChildrenCategories(tnp,tcs,0)
    return tcs


def getChildrenCategories(tcategory,tcs,tlength):
    tlength += 1
    t_childs=tcategory.parent_category.order_by('id')
    if t_childs:
        for tc in t_childs:
            tcs.append((tc.id,'--'*tlength+tc.name))
            tcs = getChildrenCategories(tc,tcs,tlength) #调用自己取下一层
    return tcs

def write_file(t_path, t_file, t_mode):
    destination = open(t_path, t_mode)
    for chunk in t_file.chunks():
        destination.write(chunk)
    destination.close()

#检查文件路径及文件名，并返回合并后的文件路径
def check_file_path(tpath, tname):
    if not os.path.exists(tpath):
        try:
            os.makedirs(tpath)
        except:
            raise 'Could not create the directory: %s' % tpath
    return tpath + tname

def get_themes():
    theme_dir = os.path.dirname(__file__)+'/../blog/templates/themes/'
    themes = os.listdir(theme_dir)
    result = []
    for theme in themes:
        if os.path.isdir(theme_dir+theme):
            result.append((theme,theme))
    return tuple(result)
