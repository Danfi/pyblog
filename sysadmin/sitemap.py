#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap
from blog.libs.articles.models import articles

class articleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return articles.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.publishTime

    def location(self, obj):
        return "/%s.html" % obj.slug

class homeSitemap(Sitemap):

    def items(self):
        return [self]

    location = "/"
    changefreq = "daily"
    priority = "1"