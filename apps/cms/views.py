import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
from django.views import View
from django.views.decorators.http import require_POST, require_GET

from apps.news.models import NewsCategory
from qiniu import Auth

from utils import restful

from apps.news.models import News
from .forms import EditNewsCategoryForm, WriteNewsForm

import qiniu
from django.utils.decorators import method_decorator


@staff_member_required(login_url='/news/index')
def index(request):
    """01 cms 后台管理首页"""
    return render(request, 'cms/index.html')

#可以看base.py源代码,dispatch其实是get,和post的父类;装饰到dispath,被get,post继承，
#那么get,post也被装饰了
@method_decorator(login_required(login_url='/account/login/'),name='dispatch')
class WriteNewsView(View):
    """02 发布新闻 页面"""
    def get(self, request):
        news_categorys = NewsCategory.objects.all()

        return render(request, 'cms/write.html',{'news_categorys':news_categorys})

    def post(self,request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            #cleaned_data 这个属性必须要调用is_valid后,
            #如果通过了,才会生成这个属性,否则没有这个属性
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')

            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title,desc=desc,
                                thumbnail=thumbnail,content=content,
                                category=category,author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())


def news_category(request):
    """03 新闻分类列表页"""
    categories = NewsCategory.objects.order_by('-id').all()
    return render(request, 'cms/news_category.html', {'categories': categories})


@require_POST
def add_news_category(request):
    """04 添加新闻分类"""
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在')

@require_POST
def modify_news_category(request):
    """05 修改新闻分类"""
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='这个分类不存在!')
    else:
        return restful.params_error(message=form.get_error())


@require_POST
def delete_news_category(request):
    """06 删除新闻分类"""
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except Exception as e:
        return restful.params_error(message='该分类不存在!')

@require_POST
def upload_file(request):
    """07 上传文件到media"""
    file = request.FILES.get('upfile')
    #print(type(file))
    #<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    if not file:
        return restful.params_error(message='没有上传任何文件')
    name = file.name
    filepath = os.path.join(settings.MEDIA_ROOT,name)
    with open(filepath,'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # /media/2.jpg
    # http://mhh4399.com:7000/media/2.jpg

    # print(request.build_absolute_uri())
    # http://mhh4399.com:7000/cms/upload_file/

    # print(request.build_absolute_uri(settings.MEDIA_URL+name))
    #http://mhh4399.com:7000/media/QQ1.png

    return restful.result(data={'url':request.build_absolute_uri(settings.MEDIA_URL+name)})

@require_GET
def qntoken(request):
    access_key = 'DzAUqfPUn2XIQuev8V6P_Piv_Gupfla_SWvnaBfd'
    secret_key = 'FQnVWzzu5L3VvkAmzshlKkkUQKwqYoPj4bBI7tc3'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = '4399abc'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name,expires=3600)
    return restful.result(data={'token':token})