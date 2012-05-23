#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from admin.decorator import admin_required
from admin.libs.files.models import blogFiles
from admin.utils import get_datatables_records
from django.utils.translation import ugettext_lazy as _

@login_required
@admin_required
def getFileList(request, template_name):
    queryset=blogFiles.objects.order_by('-uploadTime')
    search_fields = ['filename']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'page_title':_('File List'),
            'search_url':reverse('getfilelist'),
            'search_field':_('Filename')
        }
    )