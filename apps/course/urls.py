from django.urls import path
from . import views

#定义应用命名空间
app_name = 'course'

urlpatterns = [
    path(r'index',views.course_index,name='index'),
    path(r'detail/<course_id>/',views.course_detail,name='course_detail'),
    path(r'course_token/',views.course_token,name='course_token'),
    path(r'course_order/',views.course_order,name='course_order'),
    path(r'notify_url/',views.notify_view,name='notify_url'),
    path(r'order_key/',views.order_key,name='order_key'),
]