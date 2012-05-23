#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from admin.libs.settings.forms import blogSettingsForm
from admin.libs.settings.models import blogSettings
from admin.decorator import admin_required
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def blogSetting(request,template_name):
    try:
        tsettings = blogSettings.objects.get(id=1)
        if request.method == 'POST':
            form = blogSettingsForm(request.POST,instance=tsettings)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('setting'))
        else:
            form = blogSettingsForm(instance=tsettings)
        vt = loader.get_template(template_name)
        c = RequestContext(
            request,
                {
                'form':form,
                'form_url':reverse('setting'),
                'page_title':_('Blog Setting'),
            }
        )
        return HttpResponse(vt.render(c))
    except blogSettings.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Settings does not exist.')},
            context_instance=RequestContext(request)
        )