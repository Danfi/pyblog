#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class blogSettings(models.Model):
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=100)
    siteurl = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    articlesPerPage = models.IntegerField()
    commentsPerPage = models.IntegerField()
    commentsOrder = models.CharField(max_length=20)
    statisticsCode = models.TextField(null=True,blank=True)


    class Meta:
        app_label = 'sysadmin'
        db_table = 'blog_setting'

    def __unicode__(self):
        return self.title