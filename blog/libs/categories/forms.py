#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.libs.categories.models import categories
from sysadmin.utils import sortCategory

class categoriesForm(forms.ModelForm):
    name = forms.CharField(label=_("Category Name"), max_length=50,widget=forms.TextInput())
    slug = forms.SlugField(label=_('Category Slug'),max_length=50,widget=forms.TextInput())
    parent = forms.IntegerField(label=_('Parent Category'),required=False,widget=forms.Select())
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
        model = categories

    def clean_parent(self):
        parent = None
        try:
            parent = categories.objects.get(id=self.cleaned_data['parent'])
        except categories.DoesNotExist:
            pass
        return parent

    def __init__(self, *args, **kwargs):
        super(categoriesForm, self).__init__(*args, **kwargs)
        self.fields['parent'].widget=forms.Select(
            choices=tuple(sortCategory())
        )

    def save(self, commit=True):
        te = super(categoriesForm, self).save(commit=False)
        if commit:
            te.save()
        return te