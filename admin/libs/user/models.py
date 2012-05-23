#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from admin.choices import userRole

class userInfo(models.Model):
    user = models.OneToOneField(User,related_name='user_info')
    nickname = models.CharField(max_length=50)
    userRole = models.CharField(max_length=20,choices=userRole)
    website = models.CharField(max_length=50,null=True,blank=True)


    class Meta:
        app_label = 'admin'
        db_table = 'user_info'

    def __unicode__(self):
        return self.user.username