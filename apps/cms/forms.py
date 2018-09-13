from apps.forms import FormMixin
from django import forms

from apps.news.models import News

from apps.course.models import Course


class EditNewsCategoryForm(forms.Form,FormMixin):
    pk = forms.IntegerField(error_messages={'required':'必须传入分类id'})
    name = forms.CharField(max_length=100,min_length=1)


#ModelForm可以指定我这个表单是为那个模型服务的
class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    class Meta:
        model = News
        fields = ('title','desc','thumbnail','content')
        error_messages = {
            'category':{
                'required':'必须传入分类id'
            }
        }

class AddCourseForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ('pub_time', 'category', 'teacher')   # exclude 是排除哪些字段

