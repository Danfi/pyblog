#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.libs.tags.models import tags

class tagsForm(forms.ModelForm):
    name = forms.CharField(label=_("Tag Name"), max_length=50,widget=forms.TextInput())
    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'class':'input-xlarge',
                'rows':5
            }
        )
    )

    class Meta:
        model = tags
        exclude = ('actionLatest',)