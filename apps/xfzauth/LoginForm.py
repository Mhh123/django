from django import forms
from django.contrib import messages
from django.core.cache import cache

from django.shortcuts import redirect
from django.urls import reverse

from apps.forms import FormMixin
from .models import User


class LoginForm(forms.Form):
    telephone = forms.CharField(max_length=11,error_messages={
        "required":"必须输入手机号码!",
        "min_length":"最少不能超过11位!"
    })
    password = forms.CharField(min_length=6,max_length=20,error_messages={
        "required":"必须输入密码!",
        "min_length":"密码最少不能少于6位",
        "max_length":"密码最多不能多于20位"
    })
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11, error_messages={
        "required": "必须输入手机号码!",
        "min_length": "最少不能超过11位!"
    })
    username = forms.CharField(max_length=20,min_length=3,error_messages={"required":"必须输入用户名!",
                                                                          "min_length":"用户名不能少于3个字符",
                                                                          "max_length":"用户名最多不能超过20个字符"
                                                                          })
    img_captcha = forms.CharField(max_length=4,min_length=4,error_messages={"required":"必须输入图形验证码"})
    password = forms.CharField(min_length=6, max_length=20, error_messages={
        "required": "必须输入密码!",
        "min_length": "密码最少不能少于6位",
        "max_length": "密码最多不能多于20位"
    })
    password1 = forms.CharField(min_length=6, max_length=20, error_messages={
        "required": "必须输入密码!",
        "min_length": "密码最少不能少于6位",
        "max_length": "密码最多不能多于20位"
    })
    sms_captcha = forms.CharField(max_length=4,min_length=4,error_messages={"required":"必须输入短信验证码"})

    #调用form.is_valid()方法的 时候，底层就回去调用clean方法，
    # 根据情况，有时我们重写celan方法

    def validate_data(self,request):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        if password != password1:
            messages.info(request,"两次输入密码不一致")
            return redirect(reverse('account:register'))

        img_captcha = cleaned_data.get('img_captcha')
        server_img_captcha = request.session.get('img_captcha')
        if img_captcha.lower() != server_img_captcha.lower():
            messages.info(request,"图形验证码错误")
            return redirect(reverse('account:register'))

        sms_captcha = cleaned_data.get('sms_captcha')
        server_sms_captcha = cache.get('sms_captcha')

        if sms_captcha.lower() != server_sms_captcha.lower():
            messages.info(request,'短信验证码错误')
            return redirect(reverse('account:register'))
        #验证用户是否存在
        telephone = cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            messages.info(request,'该手机号码已存在')
            return redirect(reverse('account:register'))
        return True