#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.libs.categories.models import categories
from blog.libs.tags.models import tags
from blog.libs.articles.models import articles
from datetime import datetime
from django.utils import timezone

class articlesForm(forms.ModelForm):
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
    abstract = forms.CharField(
        label=_("Abstract"),
        required=False,
        widget=forms.Textarea(
            attrs={
                'style':'width:96%;height:200px;'
            }
        )
    )
    tags = forms.CharField(
        label=_("Tags"),
        required=False,
        widget=forms.TextInput()
    )
    categories = forms.ModelMultipleChoiceField(
        label=_("Categories"),
        queryset=categories.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class':'category_cbx'
            }
        )
    )
    sticky = forms.BooleanField(
        label=_("Sticky"),
        required=False,
        initial=False,
        widget=forms.CheckboxInput()
    )
    allowComment = forms.BooleanField(
        label=_("Allow Comment"),
        required=False,
        initial=True,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = articles
        exclude = ('readTimes','author','publishTime','status','type')

    def clean_tags(self):
        ttags = self.cleaned_data['tags']
        if ttags:
            id_list = []
            for t in ttags.split(','):
                if t:
                    tl,created = tags.objects.get_or_create(name=t)
                    if created:
                        tl.slug = t
                    tl.save()
                    id_list.append(tl.id)
            taglist = tags.objects.filter(id__in=id_list)
            return taglist
        return []

    def save(self,request,act_type,commit=True):
        te = super(articlesForm, self).save(commit=False)
        if commit:
            te.type = 'article'
            te.author = request.user
            if act_type == 'publish':
                if not te.publishTime:
                    te.publishTime = datetime.now(tz=timezone.get_default_timezone())
                te.status = 'Published'
            elif act_type == 'save':
                if not te.publishTime:
                    te.status = 'Saved'
            te.save()
        return te