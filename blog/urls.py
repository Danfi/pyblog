#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
)

urlpatterns += patterns('blog.views',
    url(r'^$', 'homePage'),
)

urlpatterns += patterns('blog.libs.articles.views',
    url(r'^getarticlelist/$', 'getArticleList', {'template_name':'articles/articleList.html'}, name='getarticlelist'),
    url(r'^addarticle/$', 'addArticle', {'template_name': 'articles/articleForm.html'}, name='addarticle'),
    url(r'^editarticle/(?P<tid>\d+)/$', 'editArticle', {'template_name': 'articles/articleForm.html'}, name='editarticle'),
    url(r'^delarticle/$', 'delArticle', name='delarticle'),
    url(r'^uploadimagesfromueditor/$', 'uploadImagesFromUeditor', name='uploadimagesfromueditor'),
    url(r'^uploadfilesfromueditor/$', 'uploadFilesFromUeditor', name='uploadfilesfromueditor'),

    url(r'^(?P<tslug>\w+).html$', 'articleView'),
    url(r'^category/(?P<tslug>\w+)/$', 'articleUnderCategory', name='category'),
    url(r'^tag/(?P<tslug>\w+)/$', 'articleUnderTag', name='tag'),
    url(r'^(?P<year>\d{4})/(?P<month>(\d{1,2})?)/$', 'articleUnderArchive'),
)

urlpatterns += patterns('blog.libs.categories.views',
    url(r'^getcategorylist/$', 'getCategoryList', {'template_name':'categories/categoryList.html'}, name='getcategorylist'),
    url(r'^addcategory/$', 'addCategory', {'template_name': 'categories/categoryForm.html'}, name='addcategory'),
    url(r'^editcategory/(?P<tid>\d+)/$', 'editCategory', {'template_name': 'categories/categoryForm.html'}, name='editcategory'),
    url(r'^delcategory/$', 'delCategory', name='delcategory'),
)

urlpatterns += patterns('blog.libs.comments.views',
    url(r'^editcomment/(?P<tid>\d+)/$', 'editComment', {'template_name': 'comments/commentForm.html'}, name='editcomment'),
    url(r'^getcommentlist/$', 'getCommentList', {'template_name':'comments/commentList.html'}, name='getcommentlist'),
    url(r'^delcomment/$', 'delComment', name='delcomment'),
    url(r'^enablecomment/$', 'enableComment', name='enablecomment'),
)

urlpatterns += patterns('blog.libs.links.views',
    url(r'^getlinklist/$', 'getLinkList', {'template_name':'links/linkList.html'}, name='getlinklist'),
    url(r'^addlink/$', 'addLink', {'template_name': 'links/linkForm.html'}, name='addlink'),
    url(r'^editlink/(?P<tid>\d+)/$', 'editLink', {'template_name': 'links/linkForm.html'}, name='editlink'),
    url(r'^dellink/$', 'delLink', name='dellink'),
)

urlpatterns += patterns('blog.libs.pages.views',
    url(r'^getpagelist/$', 'getPageList', {'template_name':'pages/pageList.html'}, name='getpagelist'),
    url(r'^addpage/$', 'addPage', {'template_name': 'pages/pageForm.html'}, name='addpage'),
    url(r'^editpage/(?P<tid>\d+)/$', 'editPage', {'template_name': 'pages/pageForm.html'}, name='editpage'),
)

urlpatterns += patterns('blog.libs.tags.views',
    url(r'^gettaglist/$', 'getTagList', {'template_name':'tags/tagList.html'}, name='gettaglist'),
    url(r'^addtag/$', 'addTag', {'template_name': 'tags/tagForm.html'}, name='addtag'),
    url(r'^edittag/(?P<tid>\d+)/$', 'editTag', {'template_name': 'tags/tagForm.html'}, name='edittag'),
    url(r'^deltag/$', 'delTag', name='deltag'),
)