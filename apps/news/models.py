from django.db import models


# Create your models here.


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


# aware time 清醒的时间(清醒的知道自己的时间代表的是哪个时区的)
# navie time 幼稚的时间(不知道自己的时间代表的是哪个时区的)

class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey("NewsCategory",
                                 on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey("xfzauth.User",
                               on_delete=models.SET_NULL,null=True)

    class Meta:
        # 每次News.objects提取数据的时候，就会按照列表中指定的字段排序
        # 加负号是倒序排序
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey("News", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("xfzauth.User", on_delete=models.CASCADE)
    class Meta:
        ordering = ['-pub_time']