from django.urls import path


from . import views


#设置app命名空间
# app_name = 'news'


urlpatterns = [
    path(r'index/',views.index,name='index'),
    path(r'news_detail/<news_id>/',views.news_detail,name='news_detail'),
    path(r'search/',views.search,name='search'),
    path(r'news_list/',views.news_list,name='news_list'),
    path(r'add_comment/',views.add_comment,name='add_comment'),
]