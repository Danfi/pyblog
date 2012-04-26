#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class categories(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,unique=True)
    parent = models.ForeignKey('self',related_name='parent_category',null=True,blank=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        app_label = 'blog'
        db_table = 'categories'

    def __unicode__(self):
        return self.name