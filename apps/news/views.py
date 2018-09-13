# Create your views here.
from collections import Iterable

from apps.news.models import News, NewsCategory
from django.conf import settings
from django.contrib.auth.decorators import login_required
# login_required 只能针对传统的页面跳转，但是不能处理ajax请求
# 也就是说，如果一个ajax请求，访问一个授权的页面
# 那么这个装饰器的页面跳转功能就不行了
from django.core import serializers
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST
from utils import restful

from apps.xfzauth.decorators import xfz_login_required
from .forms import AddCommentForm
from .models import Comment

from .serializers import NewsSerializer,CommentSerializer

def index(request):
    # news = News.objects.all()
    categories = NewsCategory.objects.all()
    # 优化,因为在html页面for 遍历变量 {{ new.category.name }}
    # 会发生sql查询,for循环次数越多机会发生越多次
    # 会拖慢数据库的查询，所以
    # 在这里需要优化
    news = News.objects.select_related('category', 'author')[0:settings.ONE_PAGE_NEWS_COUNT]
    # print(type(news))   #<class 'django.db.models.query.QuerySet'>
    # print(news) #<QuerySet [<News: News object (1)>, <News: News object (4)>, <News: News object (5)>]>

    context = {
        'news': news,
        'categories': categories
    }

    return render(request, 'news/index.html', context=context)


@require_GET
def news_list(request):
    # /new/list/?p=3
    page = request.GET.get('p', 1)
    category_id = int(request.GET.get('category_id', 0))
    # offer, limit
    start = settings.ONE_PAGE_NEWS_COUNT * (int(page) - 1)
    end = start + settings.ONE_PAGE_NEWS_COUNT

    # newses = News.objects.all()[start:end].values()
    #  <class 'django.db.models.query.QuerySet'>
    # QuerySet 是可迭代的

    # newses = serializers.serialize('json', newses)
    if category_id == 0:
        # 如果category_id=0,说明没有传category_id过来
        newses = News.objects.all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)

    # print(type(serializer)) # <class 'rest_framework.serializers.ListSerializer'>
    return restful.result(data=serializer.data)


# 如果在url中定义了参数
# 那么在视图函数中也要定义相应的参数
def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404

@require_POST
@xfz_login_required
def add_comment(request):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news,
                                         author=request.user)
        serializer = CommentSerializer(comment)
        # 这一这里并没有指定many=True,
        # 因为comment并不是一个Queryset对象；
        # 只是一个普通对象
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_error())
def search(request):
    return render(request, 'news/search.html')
