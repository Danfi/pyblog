#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from sysadmin.choices import userRole, userStatus
from sysadmin.decorator import admin_required
from sysadmin.libs.user.forms import newUserForm, editPasswordForm, editUserForm, registerUserForm
from sysadmin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

def registerUser(request, template_name):
    if request.method == 'POST':
        form = registerUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = registerUserForm()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('registeruser'),
            'page_title':_('Register User')
        }
    )
    return HttpResponse(vt.render(c))

@login_required
@admin_required
def getUserList(request, template_name):
    queryset=User.objects.all()
    search_fields = ['username','email']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'userRole':userRole,
            'userStatus':userStatus,
            'tstatus':_('Status'),
            'page_title':_('User List'),
            'search_url':reverse('getuserlist'),
            'search_field':_('Username,Email')
        }
    )

@login_required
@admin_required
def addUser(request, template_name):
    if request.method == 'POST':
        form = newUserForm(request,request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(reverse('getuserlist'))
    else:
        form = newUserForm(request)
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('adduser'),
            'page_title':_('Add User')
        }
    )
    return HttpResponse(vt.render(c))

@login_required
def editUser(request, tid,template_name):
    try:
        tuser = User.objects.get(id=tid)
        if request.method == 'POST':
            form = editUserForm(request,tuser,request.POST)
            if form.is_valid():
                form.save(tuser)
                return HttpResponseRedirect(reverse('edituser',args=[tid]))
        else:
            t_initial = {
                'email':tuser.email,
                'nickname':tuser.user_info.nickname,
                'website':tuser.user_info.website,
            }
            form = editUserForm(request,tuser,initial=t_initial)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
            {
                'form':form,
                'tid':tid,
                'form_url':reverse('edituser',args=[tid]),
                'page_title':_('Edit User')
            }
        )
        return HttpResponse(vt.render(c))
    except User.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('User does not exist.')},
            context_instance=RequestContext(request)
        )

@login_required
def editPassword(request, template_name):
    if request.method == 'POST':
        form = editPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin'))
    else:
        form = editPasswordForm(request.user)
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('editpassword'),
            'page_title':_('Edit Password')
        }
    )
    return HttpResponse(vt.render(c))

@csrf_exempt
@login_required
@admin_required
def delUser(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            User.objects.filter(id__in=tids).delete()
    return HttpResponseRedirect(reverse('getuserlist'))