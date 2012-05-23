#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url, handler404, handler500
from django.conf import settings
from admin.feeds import LatestEntriesFeed
from admin.sitemap import articleSitemap, homeSitemap


sitemaps = {
    'blog': articleSitemap,
    'home':homeSitemap
}

urlpatterns = patterns('',
    url(r'^', include('admin.urls')),
    url(r'^', include('blog.urls')),
    # Examples:
    # url(r'^$', 'pyblog.views.home', name='home'),
    # url(r'^pyblog/', include('pyblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
    (r'^feed/$', LatestEntriesFeed()),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^uploadfiles/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

handler404 = 'admin.libs.error.views.error404'
handler500 = 'admin.libs.error.views.error500'