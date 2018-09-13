# encoding:utf-8
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone, username, password, **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    gender = models.IntegerField(default=0)  # 0位置 1男 2女
    date_join = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    # USERNAME_FIELD :这个属性是以后在使用authenticate
    # 进行验证的字段
    USERNAME_FIELD = 'telephone'
    # 这个属性用来，以后在命令行中使用createsuperuser命令
    # 的时候，会让你输入的字段
    REQUIRED_FIELDS = ['username']
    # 以后给每个用户发送邮箱的时候，就会使用这个属性指定的字段值来发送
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
