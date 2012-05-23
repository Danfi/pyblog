#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import urllib

from django.db import models
from blog.libs.articles.models import articles
from admin.choices import commentsStatus

class comments(models.Model):
    no = models.IntegerField()
    submitTime = models.DateTimeField()
    article = models.ForeignKey(articles,related_name='article_comments')
    username = models.CharField(max_length=60)
    email = models.EmailField()
    website = models.CharField(max_length=100,blank=True,null=True)
    content = models.TextField()
    status = models.CharField(max_length=20,choices=commentsStatus)

    class Meta:
        app_label = 'blog'
        db_table = 'comments'

    def __unicode__(self):
        return self.username

    def gravatar_url(self):
        default='identicon'
        if not self.email:
            return default
        size = 50
        try:
            imgurl = "http://www.gravatar.com/avatar/"
            imgurl +=hashlib.md5(self.email.lower()).hexdigest()+"?"+ urllib.urlencode({
                'd':default, 's':str(size),'r':'G'})
            return imgurl
        except:
            return default

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.no = int(max([int(x) for x in comments.objects.values_list('no',flat=True)]))+1
            except ValueError:
                self.no = 1
            self.status = 'Enabled'
        super(comments, self).save(*args, **kwargs)