#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class tags(models.Model):
    name = models.CharField(max_length=50,unique=True)
    actionLatest = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        app_label = 'blog'
        db_table = 'tags'

    def __unicode__(self):
        return self.name