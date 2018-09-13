from django.urls import path

from . import views
from . import course_views

app_name = 'cms'

urlpatterns = [
    path(r'index/',views.index,name='index'),
    path(r'write_news/',views.WriteNewsView.as_view(),name='write_news'),
    path(r'news_category/',views.news_category,name='news_category'),
    path(r'add_news_category/',views.add_news_category,name='add_news_category'),
    path(r'modify_news_category/',views.modify_news_category,name='modify_news_category'),
    path(r'delete_news_category/',views.delete_news_category,name='delete_news_category'),
    path(r'upload_file/',views.upload_file,name='upload_file'),
    path(r'qntoken/',views.qntoken,name='qntoken'),
]

# 课程相关的url配置
urlpatterns += [
    path(r'pub_course/',course_views.PubCourse.as_view(), name='pub_course'),
]