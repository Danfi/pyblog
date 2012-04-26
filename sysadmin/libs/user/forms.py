#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from sysadmin.libs.user.models import userInfo
from sysadmin.choices import userRole

class registerUserForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',widget=forms.TextInput())
    email = forms.EmailField(label=_('Mail Address'), max_length=75, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    passwordConfirm = forms.CharField(label=_("Password Confirm"), widget=forms.PasswordInput())

    class Meta:
        model = User
        exclude = ('first_name','last_name','groups','user_permissions','is_staff','is_active','is_superuser','last_login','date_joined',)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_passwordConfirm(self):
        password = self.cleaned_data["password"]
        passwordConfirm = self.cleaned_data["passwordConfirm"]
        if password != passwordConfirm:
            raise forms.ValidationError(_('Passwords are not the same.'))
        return passwordConfirm

    def save(self, commit=True):
        user = super(registerUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.first_name = self.cleaned_data["username"]
            user.last_name = 'reader'
            user.save()
        userInfo.objects.create(user=user,nickname=user.username,userRole='reader')
        return user

registerUserForm.base_fields.keyOrder = ['username','email','password','passwordConfirm']

class newUserForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^\w+$',widget=forms.TextInput())
    email = forms.EmailField(label=_('Mail Address'), max_length=75, widget=forms.TextInput())
    nickname = forms.CharField(label=_('Nickname'), required=False, max_length=30, widget=forms.TextInput())
    website = forms.URLField(label=_('Website'), required=False, max_length=50, widget=forms.TextInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())
    passwordConfirm = forms.CharField(label=_("Password Confirm"), widget=forms.PasswordInput())

    class Meta:
        model = User
        exclude = ('last_name','first_name','groups','user_permissions','is_staff',
                   'is_active','is_superuser','last_login','date_joined',)

    def __init__(self, request, *args, **kwargs):
        super(newUserForm, self).__init__(*args, **kwargs)
        baseOrder = ['username','email','nickname','website','password','passwordConfirm']
        if request.user.get_user_role() == 'admin':
            self.fields['userRole'] = forms.CharField(label=_('User Role'), max_length=30, widget=forms.Select(choices=userRole))
            baseOrder.insert(3, 'userRole')
        self.fields.keyOrder = baseOrder

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_passwordConfirm(self):
        password = self.cleaned_data["password"]
        passwordConfirm = self.cleaned_data["passwordConfirm"]
        if password != passwordConfirm:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return passwordConfirm

    def save(self, request, commit=True):
        user = super(newUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        tuserinfo = userInfo.objects.create(user=user)
        if request.user.get_user_role() == 'admin':
            tuserinfo.userRole = self.cleaned_data["userRole"]
        else:
            tuserinfo.userRole = 'reader'
        if self.cleaned_data["nickname"]:
            tuserinfo.nickname = self.cleaned_data["nickname"]
        if self.cleaned_data["website"]:
            tuserinfo.website = self.cleaned_data["website"]
        tuserinfo.save()
        return user

class editUserForm(forms.Form):
    email = forms.EmailField(label=_('Mail Address'), max_length=75, widget=forms.TextInput())
    nickname = forms.CharField(label=_('Nickname'), required=False, max_length=30, widget=forms.TextInput())
    website = forms.URLField(label=_('Website'), required=False, max_length=50, widget=forms.TextInput())
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput())
    new_password1 = forms.CharField(label=_("New password"), required=False, widget=forms.PasswordInput())
    new_password2 = forms.CharField(label=_("New password confirmation"), required=False, widget=forms.PasswordInput())

    def __init__(self,request,tuser, *args, **kwargs):
        self.user = tuser
        super(editUserForm, self).__init__(*args, **kwargs)
        baseOrder = ['email','nickname','website','old_password','new_password1','new_password2']
        if request.user.get_user_role() == 'admin':
            self.fields['userRole'] = forms.CharField(label=_('User Role'), max_length=30, widget=forms.Select(choices=userRole))
            baseOrder.insert(3, 'userRole')
        self.fields.keyOrder = baseOrder

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Password was entered incorrectly. Please enter it again."))
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_website(self):
        website = self.cleaned_data['website']
        if website:
            if not website.startswith(('http://','https://')):
                website = 'http://' + website
        return website

    def save(self, tuser, commit=True):
        tuser.email = self.cleaned_data["email"]
        tuser.save()
        tuserinfo = tuser.user_info
        try :
            tuserinfo.userRole = self.cleaned_data["userRole"]
        except:
            pass
        if self.cleaned_data["nickname"]:
            tuserinfo.nickname = self.cleaned_data["nickname"]
        if self.cleaned_data["website"]:
            tuserinfo.website = self.cleaned_data["website"]
        tuserinfo.save()
        if self.cleaned_data["new_password1"]:
            tuser.set_password(self.cleaned_data["new_password1"])
        return tuser

class editPasswordForm(forms.Form):
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput())
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput())
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput())

    def __init__(self, tuser, *args, **kwargs):
        self.user = tuser
        super(editPasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user