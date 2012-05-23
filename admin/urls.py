#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url':'/'}, name='logout'),
)

urlpatterns += patterns('admin.libs.files.views',
    url(r'^getfilelist/$', 'getFileList', {'template_name':'files/fileList.html'}, name='getfilelist'),
)

urlpatterns += patterns('admin.libs.login.views',
    url(r'^login/$', 'login', {'template_name':'login/login.html'}, name='login'),
    url(r'^admin/$', 'admin', {'template_name':'login/admin.html'}, name='admin'),
)

urlpatterns += patterns('admin.libs.settings.views',
    url(r'^setting/$', 'blogSetting', {'template_name':'blogSetting/blogSettingForm.html'}, name='setting'),
)

urlpatterns += patterns('admin.libs.user.views',
    url(r'^registeruser/$', 'registerUser', {'template_name':'user/registerUserForm.html'}, name='registeruser'),
    url(r'^adduser/$', 'addUser', {'template_name':'user/addUserForm.html'}, name='adduser'),
    url(r'^edituser/(?P<tid>\d+)/$', 'editUser', {'template_name':'user/editUserForm.html'}, name='edituser'),
    url(r'^getuserlist/$','getUserList', {'template_name':'user/userList.html'}, name='getuserlist'),
    url(r'^editpassword/$','editPassword', {'template_name':'user/editPasswordForm.html'}, name='editpassword'),
    url(r'^deluser/$', 'delUser', name='deluser'),
)