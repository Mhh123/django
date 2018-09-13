#encoding: utf-8
from django import forms

from apps.forms import FormMixin

class AddCommentForm(forms.Form,FormMixin):
    # 在表单中，charField和TextField唯一的区别
    # 在表单渲染成模板的时候会有区别，
    # charField会被渲染成input标签
    # TextField会被渲染成Textarea
    content = forms.CharField()
    news_id = forms.IntegerField()