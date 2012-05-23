#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from blog.libs.categories.models import categories
from blog.libs.comments.forms import commentsForm
from blog.libs.tags.models import tags
from django.utils import simplejson
from forms import articlesForm
from blog.libs.articles.models import articles
from admin.decorator import admin_required, writer_required
from admin.libs.files.models import blogFiles
from admin.utils import get_datatables_records, write_file, check_file_path, getBlogTheme
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.conf import settings
import os, random
from PIL import Image
from admin.libs.settings.models import blogSettings

@login_required
@writer_required
def addArticle(request, template_name):
    act_type = 'publish'
    try:
        if request.GET['act_type']:
            act_type = request.GET['act_type']
    except MultiValueDictKeyError:
        pass
    if request.method == 'POST':
        form = articlesForm(request.POST)
        if form.is_valid():
            t = form.save(request,act_type)
            form.save_m2m()
            if act_type == 'publish':
                return HttpResponseRedirect(reverse('getarticlelist'))
            elif act_type == 'save':
                return HttpResponseRedirect(reverse('editarticle',args=[t.id]))
    else:
        form = articlesForm()
    vt = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'form':form,
            'form_url':reverse('addarticle'),
            'page_title':_('Add Article'),
            'tags':tags.objects.order_by('-actionLatest')[0:35],
            'tslug':None
        }
    )
    return HttpResponse(vt.render(c))

@login_required
def editArticle(request,tid,template_name):
    act_type = 'publish'
    try:
        if request.GET['act_type']:
            act_type = request.GET['act_type']
    except MultiValueDictKeyError:
        pass
    try:
        tarticles = articles.objects.get(id=tid)
        if tarticles.author == request.user or request.user.get_user_role() == 'admin':
            if request.method == 'POST':
                form = articlesForm(request.POST,instance=tarticles)
                if form.is_valid():
                    t = form.save(request,act_type)
                    form.save_m2m()
                    if act_type == 'publish':
                        return HttpResponseRedirect(reverse('getarticlelist'))
                    elif act_type == 'save':
                        return HttpResponseRedirect(reverse('editarticle',args=[t.id]))
            else:
                taglist = tarticles.tags.values_list('name',flat=True)
                tag_init = ','.join(taglist)
                if tag_init:
                    tag_init += ','
                form = articlesForm(instance=tarticles,initial={'tags':tag_init})
            vt = loader.get_template(template_name)
            c = RequestContext(
                request,
                    {
                    'form':form,
                    'form_url':reverse('editarticle',args=[tid]),
                    'page_title':_('Edit Article'),
                    'tags':tags.objects.all()[0:35],
                    'tslug':tarticles.slug
                }
            )
            return HttpResponse(vt.render(c))
        return render_to_response(
            'error.html',
            {'message':_('You have no perm to edit this article.')},
            context_instance=RequestContext(request)
        )
    except articles.DoesNotExist:
        return render_to_response(
            'error.html',
                {'message':_('Article does not exist.')},
            context_instance=RequestContext(request)
        )

@login_required
@writer_required
def getArticleList(request, template_name):
    queryset=articles.objects.filter(type='article').order_by('-publishTime')
    if request.user.get_user_role() == 'writer':
        queryset = queryset.filter(author=request.user)
    search_fields = ['title']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        template_name,
        extra_context={
            'page_title':_('Article List'),
            'search_url':reverse('getarticlelist'),
            'search_field':_('Title')
        }
    )

@csrf_exempt
@login_required
@admin_required
def delArticle(request):
    if request.method == 'POST':
        tids = request.POST.getlist('tids[]')
        if len(tids)>0:
            articles.objects.filter(id__in=tids).delete()
    return HttpResponseRedirect(reverse('getarticlelist'))

def articleView(request,tslug):
    try:
        tarticle = articles.objects.get(slug=tslug)
        tblogSettings = blogSettings.objects.get(id=1)
        tcomments = tarticle.article_comments.all()
        if tblogSettings.commentsOrder == 'descending':
            tcomments = tcomments.order_by('-submitTime')
        page_result = Paginator(tcomments, tblogSettings.commentsPerPage)
        page_range = page_result.page_range
        try:
            page = int(request.GET.get('page', '1'))
            if page not in page_range:
                page = 1
        except ValueError:
            page = 1
        t_page = page_result.page(page)
        object_result = t_page.object_list
        if t_page.has_previous():
            prev_page = page - 1
        else:
            prev_page = 0
        if t_page.has_next():
            next_page = page + 1
        else:
            next_page = 0
        if request.method == 'POST':
            number1 = int(request.POST['number1'])
            number2 = int(request.POST['number2'])
            arithmeticResult = number1 + number2
            form = commentsForm(arithmeticResult,request.POST)
            if form.is_valid():
                form.save(tarticle,'add')
                return HttpResponseRedirect('/%s.html' %tslug)
        else:
            number1 = random.randint(1, 10)
            number2 = random.randint(1, 10)
            arithmeticResult = number1 + number2
            form = commentsForm(arithmeticResult)
        vt = loader.get_template('themes/'+getBlogTheme()+'/article.html')
        c = RequestContext(
            request,
            {
                'article':tarticle,
                'tslug':tslug,
                'tcomments':object_result,
                'prev_page': prev_page,
                'page':page,
                'next_page': next_page,
                'form':form,
                'number1':number1,
                'number2':number2
            }
        )
        return HttpResponse(vt.render(c))
    except articles.DoesNotExist:
        return render_to_response(
            'themes/default/error.html',
                {'message':_('Article does not exist.')},
            context_instance=RequestContext(request)
        )

def articleUnderCategory(request,tslug):
        try:
            tcategory = categories.objects.get(slug=tslug)
            queryset=articles.objects.filter(categories=tcategory,type='article').order_by('-publishTime')
            search_fields = ['title']
            return get_datatables_records(
                request,
                queryset,
                search_fields,
                'themes/'+getBlogTheme()+'/category.html',
                extra_context={
                    'category':tcategory
                }
            )
        except categories.DoesNotExist:
            return render_to_response(
                'themes/'+getBlogTheme()+'/category.html',
                    {'message':_('Category does not exist.')},
                context_instance=RequestContext(request)
            )

def articleUnderTag(request,tslug):
    try:
        ttag = tags.objects.get(name=tslug)
        queryset=articles.objects.filter(tags=ttag,type='article').order_by('-publishTime')
        search_fields = ['title']
        return get_datatables_records(
            request,
            queryset,
            search_fields,
            'themes/'+getBlogTheme()+'/tag.html',
            extra_context={
                'tag':ttag
            }
        )
    except tags.DoesNotExist:
        return render_to_response(
            'themes/'+getBlogTheme()+'/tag.html',
                {'message':_('Tag does not exist.')},
            context_instance=RequestContext(request)
        )

def articleUnderArchive(request,year,month):
    queryset=articles.objects.filter(publishTime__year=year,publishTime__month=month,type='article').order_by('-publishTime')
    search_fields = ['title']
    return get_datatables_records(
        request,
        queryset,
        search_fields,
        'themes/'+getBlogTheme()+'/archive.html',
        extra_context={
            'year':year,
            'month':month
        }
    )

@csrf_exempt
@login_required
@admin_required
def uploadImagesFromUeditor(request):
    if request.method == 'POST' and request.FILES.values():
        results = {}
        for t_file in request.FILES.values():
            try:
                title = request.POST['pictitle']
            except MultiValueDictKeyError:
                title = t_file.name
            tpath = datetime.now().strftime('%Y/%m/%d/')
            r_path = os.path.join(settings.MEDIA_ROOT, tpath)
            tname = datetime.now().strftime('%H%M%S%f') + '%s' % random.randrange(1, 10000)+ '.' + t_file.name.rsplit('.',1)[1]
            write_file(check_file_path(r_path, tname), t_file, 'wb+')
            image_path = os.path.join(tpath, tname)
            blogFiles.objects.create(filename=t_file.name,fileUrl=image_path,uploadTime=datetime.now())
            image = Image.open(os.path.join(r_path, tname))
            if image.size[0] > 450:
                thumb_name = 'thumb_'+tname
                thumb_height = 450/float(image.size[0])*float(image.size[1])
                image = image.resize((450, int(thumb_height)), Image.ANTIALIAS)
                image.save(os.path.join(r_path, thumb_name))
                image_path = os.path.join(tpath, thumb_name)

            results['url'] = image_path
            results['title'] = title
            results['state'] = 'SUCCESS'
    return HttpResponse(simplejson.dumps(results, ensure_ascii = False), mimetype = 'application/json')

@csrf_exempt
def uploadFilesFromUeditor(request):
    if request.method == 'POST' and request.FILES.values():
        results = {}
        for t_file in request.FILES.values():
            try:
                title = request.POST['pictitle']
            except MultiValueDictKeyError:
                title = t_file.name
            tpath = datetime.now().strftime('%Y/%m/%d/')
            r_path = os.path.join(settings.MEDIA_ROOT, tpath)
            tname = datetime.now().strftime('%H%M%S%f') + '%s' % random.randrange(1, 10000)+ '.' + t_file.name.rsplit('.',1)[1]
            write_file(check_file_path(r_path, tname), t_file, 'wb+')
            file_path = os.path.join(tpath, tname)
            blogFiles.objects.create(filename=t_file.name,fileUrl=file_path,uploadTime=datetime.now())
            results['url'] = file_path
            results['title'] = title
            results['state'] = 'SUCCESS'
    return HttpResponse(simplejson.dumps(results, ensure_ascii = False), mimetype = 'application/json')