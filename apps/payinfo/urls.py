from django.urls import path


from . import views

app_name = 'payinfo'

urlpatterns = [
    path(r'pay_info',views.pay_info,name='pay_info')
]