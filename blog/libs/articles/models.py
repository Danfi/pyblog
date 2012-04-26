#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from blog.libs.categories.models import categories
from blog.libs.tags.models import tags
from django.contrib.auth.models import User

class articles(models.Model):
    title = models.CharField(max_length=60)
    type = models.CharField(max_length=20)
    slug = models.SlugField(max_length=50,unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(tags,related_name='article_tags',null=True,blank=True)
    categories = models.ManyToManyField(categories,related_name='article_categories',null=True,blank=True)
    publishTime = models.DateTimeField(null=True,blank=True)
    author = models.ForeignKey(User,related_name='article_author')
    readTimes = models.IntegerField(default=0)
    sticky = models.BooleanField()
    allowComment = models.BooleanField()
    status = models.CharField(max_length=20)
    abstract = models.CharField(max_length=1000,blank=True,null=True)

    class Meta:
        app_label = 'blog'
        db_table = 'articles'

    def __unicode__(self):
        return self.title