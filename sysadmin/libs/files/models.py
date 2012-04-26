#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class blogFiles(models.Model):
    filename = models.CharField(max_length=256)
    fileUrl = models.CharField(max_length=512)
    uploadTime = models.DateTimeField()

    class Meta:
        app_label = 'sysadmin'
        db_table = 'blog_files'

    def __unicode__(self):
        return self.filename