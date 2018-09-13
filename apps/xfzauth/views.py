# encoding:utf-8
import json
from string import printable

from django.contrib.messages import get_messages
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from random import choice
from django.contrib.auth import logout

from utils.captcha.captcha import create_captcha

from .models import User
from .LoginForm import LoginForm,RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from utils.dysms_python.demo_sms_send import send_sms

# def login_view(request):
#     if request.method == 'GET':
#         return render(request,'auth/login.html')


class LoginView(View):
    """01登录函数"""
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = authenticate(request, username=telephone, password=password)

            if user:
                login(request, user)
                if remember:
                    # 如果没设置过期时间为None，那么使用默认的过期时间
                    # 默认的过期时间是2个礼拜，也就是14天
                    request.session.set_expiry(None)
                else:
                    # 如果设置过期时间为0，那么浏览器关闭以后就会结束
                    request.session.set_expiry(0)
                return redirect(reverse('news:index'))
            else:
                messages.info(request,'用户名或密码错误')

                return redirect(reverse('account:login'))
        else:
            messages.info(request,'表单验证失败')
            return redirect(reverse('account:login'))


class Register(View):
    """02注册函数"""
    def get(self,request):
        return render(request,'auth/register.html')
    def post(self,request):
        form = RegisterForm(request.POST)

        #逻辑上先验证数据有效
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #然后判断图形码，短信吗，二次密码
            if form.validate_data(request):
                user = User.objects.create_user(telephone=telephone,
                                                username=username,password=password)
                if user:
                    login(request,user)
                    return redirect(reverse('news:index'))
                else:
                    messages.info(request,'user 不存在,注册失败')
                    return redirect(reverse('account:register'))
        else:
            message = form.get_error()
            messages.info(request,message)
            return redirect(reverse('account:register'))


def img_captcha(request):
    """03图形验证码"""
    text,image = create_captcha()


    request.session['img_captcha'] = text
    # # 将图形验证码存储在session中
    request.session.set_expiry(None)
    # #设置验证码过期时间为None

    # cache.set('captcha',text,timeout=22)
    #注意这里的key，由于django cache的机制，到redis中就变成了":1:captcha"
    #django redis cache的key是由前缀：版本号：真正的key组成
    #但是，我们获取的时候还是用cache.get('captcha')
    return HttpResponse(image,content_type='image/png')

def sms_captcha(request):
    """04短信验证码"""
    telephone = request.GET.get('telephone')


    #生成随机验证码
    code = ''.join([choice(printable[:62]) for i in range(4)])

    #redis存储随机验证码
    cache.set('sms_captcha',code,timeout=120)
    result = send_sms(telephone,code).decode('utf-8')

    # print(result)
    #{"Message":"OK",
    # "RequestId":"A3AA09E0-528E-4446-AD07-0C2D4258BA4B",
    # "BizId":"454008730675547445^0","Code":"OK"}
    #print(type(result)) #<class 'str'>
    res = json.loads(result)
    # print(type(res)) #<class 'dict'>
    return HttpResponse(res["Message"])


def logout_view(request):
    """05退出账户"""
    logout(request)
    return redirect(reverse('news:index'))