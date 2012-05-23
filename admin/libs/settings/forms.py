#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from admin.libs.settings.models import blogSettings
from admin.choices import commentsOrder
from admin.utils import get_themes

class blogSettingsForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Blog Title"),
        max_length=60,
        widget=forms.TextInput(
            attrs = {
                'class':'input-xlarge',
            }
        )
    )
    subtitle = forms.CharField(
        label=_("Subtitle"),
        max_length=60,
        widget=forms.TextInput(
            attrs = {
                'class':'input-xlarge',
            }
        )
    )
    siteurl = forms.CharField(
        label=_("Site Url"),
        max_length=100,
        widget=forms.TextInput(
            attrs = {
                'class':'input-xlarge',
                }
        )
    )
    description = forms.CharField(
        label=_("Description"),
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs = {
                'class':'input-xlarge',
                'rows':5
            }
        )
    )
    articlesPerPage = forms.IntegerField(
        label=_("Articles Per Page"),
        widget=forms.TextInput(
            attrs = {
                'class':'span1',
            }
        )
    )
    commentsPerPage = forms.IntegerField(
        label=_("Comments Per Page"),
        widget=forms.TextInput(
            attrs = {
                'class':'span1',
            }
        )
    )
    commentsOrder = forms.CharField(
        label=_("Comments Order"),
        widget=forms.RadioSelect(
            choices=commentsOrder,
            attrs = {
                'class':'commentsorder',
            }
        )
    )
    statisticsCode = forms.CharField(
        label=_("Statistics Code"),
        max_length=1000,
        required=False,
        widget=forms.Textarea(
            attrs = {
                'class':'input-xlarge',
                'rows':5
            }
        )
    )
    theme = forms.CharField(
        label=_('Theme'),
        widget=forms.Select()
    )

    class Meta:
        model = blogSettings

    def __init__(self, *args, **kwargs):
        super(blogSettingsForm, self).__init__(*args, **kwargs)
        self.fields['theme'].widget=forms.Select(
            choices=get_themes(),
            attrs={
                'class':'span2'
            }
        )

    def save(self,commit=True):
        te = super(blogSettingsForm, self).save(commit=False)
        if commit:
            te.save()
        tsite = Site.objects.get(id=1)
        tsite.name = te.title
        tsite.domain = te.siteurl
        tsite.save()
        return te