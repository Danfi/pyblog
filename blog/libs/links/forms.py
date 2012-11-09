#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.libs.links.models import links

class linksForm(forms.ModelForm):
    name = forms.CharField(label=_("Link Name"), max_length=50,widget=forms.TextInput())
    url = forms.URLField(label=_('Link Url'),
        max_length=60,
        initial='http://',
        widget=forms.TextInput(
            attrs={
                'placeholder':'Do not forget http://'
            }
    ))
    description = forms.CharField(label=_("Description"), max_length=100, required=False, widget=forms.TextInput())

    class Meta:
        model = links