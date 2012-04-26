#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.libs.articles.models import articles
from datetime import datetime

class pageForm(forms.ModelForm):
    title = forms.CharField(
        label=_("Title"),
        max_length=60,
        widget=forms.TextInput(
            attrs = {
                'class':'input-xlarge',
                'style':'width:96%'
            }
        )
    )
    slug = forms.SlugField(label=_('Articles Slug'),max_length=50,widget=forms.TextInput())
    content = forms.CharField(
        label=_("Content"),
        widget=forms.Textarea(
            attrs={
                'style':'width:97%;height:425px;'
            }
        )
    )
    allowComment = forms.BooleanField(
        label=_("Allow Comment"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = articles
        exclude = ('readTimes','author','publishTime','status','type','abstract','tags','categories','sticky')

    def save(self,request,act_type,commit=True):
        te = super(pageForm, self).save(commit=False)
        if commit:
            te.type = 'page'
            te.author = request.user
            if act_type == 'publish':
                if not te.publishTime:
                    te.publishTime = datetime.now()
                te.status = 'Published'
            elif act_type == 'save':
                if not te.publishTime:
                    te.status = 'Saved'
            te.save()
        return te