#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.cache import never_cache
from admin.decorator import login_redirected
from admin.libs.login.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

@never_cache
@login_redirected
def login(request, template_name, redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action."
    redirect_to = request.REQUEST.get(redirect_field_name, settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if not redirect_to or '//' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = AuthenticationForm(request)
        request.session.set_test_cookie()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form': form,
            'form_url':reverse('login'),
            redirect_field_name: redirect_to,
            'page_title':_('User Login')
        }
    )
    return HttpResponse(vt.render(c))

@login_required
def admin(request,template_name):
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'page_title':_('Admin Home')
        }
    )
    return HttpResponse(vt.render(c))