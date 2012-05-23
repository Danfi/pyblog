#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from django.utils import timezone
from django import forms
from django.utils.translation import ugettext_lazy as _
from blog.libs.comments.models import comments

class commentsForm(forms.ModelForm):
    username = forms.CharField(
        label=_('Username'),
        max_length=60,
        widget=forms.TextInput(
            attrs={
                'size':24
            }
        )
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.TextInput(
            attrs={
                'size':24
            }
        )
    )
    arithmetic = forms.IntegerField(
        label=_('Arithmetic'),
        widget=forms.TextInput(
            attrs={
                'size':24
            }
        )
    )
    website = forms.CharField(
        label=_('Website'),
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'size':24
            }
        )
    )
    content = forms.CharField(
        label=_('Content'),
        widget=forms.Textarea(
            attrs={
                'row':10,
                'cols':79
            }
        )
    )

    class Meta:
        model = comments
        exclude =('article','no','submitTime','status')

    def __init__(self, arithmeticResult=None, *args, **kwargs):
        self.arithmeticResult = arithmeticResult
        super(commentsForm, self).__init__(*args, **kwargs)
        if arithmeticResult:
            self.fields['arithmetic'] = forms.IntegerField(
                label=_('Arithmetic'),
                widget=forms.TextInput(
                    attrs={
                        'size':24
                    }
                )
            )

    def clean_website(self):
        website = self.cleaned_data['website']
        if website:
            if not website.startswith(('http://','https://')):
                website = 'http://' + website
        return website

    def clean_arithmetic(self):
        arithmetic = self.cleaned_data['arithmetic']
        if arithmetic != self.arithmeticResult:
            raise forms.ValidationError(_("The answer is wrong."))
        return arithmetic

    def save(self,article,taction,commit=True):
        te = super(commentsForm, self).save(commit=False)
        if commit:
            if taction == 'add':
                te.article = article
                te.submitTime = datetime.now(tz=timezone.get_default_timezone())
            te.save()
        return te