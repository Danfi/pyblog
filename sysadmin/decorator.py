#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext_lazy as _

def login_redirected(func):
    def _decorator(request, *args, **kwargs):
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect_to)
        else:
            return func(request, *args, **kwargs)
    return _decorator

def admin_required(func):
    def _decorator(request, *args, **kwargs):
        if request.user.get_user_role() == 'admin':
            return func(request, *args, **kwargs)
        else:
            return render_to_response(
                'error.html',
                {
                    'message':_('You have no perm to edit this article.'),
                },
                context_instance=RequestContext(request)
            )
    return _decorator

def writer_required(func):
    def _decorator(request, *args, **kwargs):
        if request.user.get_user_role() in ['admin','writer']:
            return func(request, *args, **kwargs)
        else:
            return render_to_response(
                'error.html',
                {
                    'message':_('You have no perm to edit this article.')
                },
                context_instance=RequestContext(request)
            )
    return _decorator