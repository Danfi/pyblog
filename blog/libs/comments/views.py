#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from blog.libs.comments.forms import commentsForm
from blog.libs.comments.models import comments
from admin.choices import commentsStatus
from admin.decorator import admin_required
from admin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def getCommentList(request, template_name):
    queryset=comments.objects.filter(status='Enabled').order_by('-submitTime')
    search_fields = []
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'commentsStatus':commentsStatus,
            'tstatus':_('Status'),
            'page_title':_('Comment List'),
            'search_url':reverse('getcommentlist'),
            'search_field':_('Content')
        }
    )

@login_required
@admin_required
def editComment(request,tid,template_name):
    try:
        tcomments = comments.objects.get(id=tid)
        if request.method == 'POST':
            form = commentsForm(request.POST,instance=tcomments)
            if form.is_valid():
                form.save(tcomments.article,'edit')
                return HttpResponseRedirect(reverse('getcommentlist'))
        else:
            form = commentsForm(instance=tcomments)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
                {
                'form':form,
                'form_url':reverse('editcomment',args=[tid]),
                'page_title':_('Edit Comment')
            }
        )
        return HttpResponse(vt.render(c))
    except comments.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Comment does not exist.')},
            context_instance=RequestContext(request)
        )

@csrf_exempt
@login_required
@admin_required
def delComment(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            comments.objects.filter(id__in=tids).delete()
    return HttpResponseRedirect(reverse('getcommentlist'))

@csrf_exempt
@login_required
@admin_required
def enableComment(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            comments.objects.filter(id__in=tids).update(status='Enabled')
    return HttpResponseRedirect(reverse('getcommentlist'))