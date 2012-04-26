#!/usr/bin/env python
# -*- coding: utf-8 -*-
from blog.libs.articles.models import articles
from blog.libs.categories.models import categories
from blog.libs.comments.models import comments
from blog.libs.links.models import links
from blog.libs.tags.models import tags
from sysadmin.libs.settings.models import blogSettings

def get_site_info(request):
    tinfo = blogSettings.objects.get(id=1)
    return {
        'title':tinfo.title,
        'description':tinfo.description,
        'statisticsCode':tinfo.statisticsCode,
        'siteurl':tinfo.siteurl,
        'categories':categories.objects.all(),
        'tags':tags.objects.all(),
        'links':links.objects.all(),
        'archives':articles.objects.dates('publishTime','month',order='DESC'),
        'pages':articles.objects.filter(type='page'),
        'recent_comments':comments.objects.order_by('-submitTime')[0:10]
    }