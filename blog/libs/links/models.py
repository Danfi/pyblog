#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class links(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=60)
    description = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        app_label = 'blog'
        db_table = 'links'

    def __unicode__(self):
        return self.name