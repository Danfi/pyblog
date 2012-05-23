#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from blog.libs.articles.models import articles
from admin.libs.settings.models import blogSettings

class LatestEntriesFeed(Feed):
    try:
        tblogSettings = blogSettings.objects.get(id=1)
        title = tblogSettings.title
        link= "http://" + tblogSettings.siteurl
        description= tblogSettings.description
    except blogSettings.DoesNotExist:
        title=  'Pyblog'
        link='http://www.pyblog.com'
        description= ''

    def items(self, obj):
        return articles.objects.order_by('-publishTime')[:10]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return '/%s.html' % item.slug