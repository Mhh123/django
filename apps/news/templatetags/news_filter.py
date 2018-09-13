from datetime import datetime

from django import template
from django.utils.timezone import now as now_func

register = template.Library()


@register.filter
def time_since(value):
    """
    time距离现在的时间间隔
    1 如果时间间隔小于1分钟，那么就显示"刚刚"
    2 如果大于1分钟小于1小时,那么就是显示"xx分钟前"
    3 如果大于1小时小于24小时，那么就显示"XX小时前"
    4 如果大于24小时小于30天以内,那么就显示"XX天前"
    5 > 30 天，就显示具体时间
    :param value:   代表发布时间
    :return:
    """
    if not isinstance(value, datetime):
        return value
    # now = datetime.now()
    now = now_func()
    # timestamp 还是datetime类型
    timestamp = (now - value).total_seconds()  # 现在距离发布时间总共多少秒
    if timestamp < 60:
        return '刚刚'
    elif timestamp >= 60 and timestamp < 60 * 60:
        minutes = int(timestamp / 60)
        return '{}分钟前'.format(minutes)
    elif timestamp >= 60 * 60 and timestamp < 60 * 60 * 24:
        hours = int(timestamp / 60 / 60)
        return '{}小时前'.format(hours)
    elif timestamp >= 60 * 60 * 24 and timestamp < 60 * 60 * 24 * 30:
        days = int(timestamp / 60 / 60 / 24)
        return '{}天前'.format(days)
    else:
        return value.strftime("%Y/%m/%d %H:%M")


"""
1 报错 原因是1 个是幼稚的时间  一个不是清醒的时间
TypeError at /news/index/
can't subtract offset-naive and offset-aware datetimes
解决:
    我们吧幼稚的时间变成清醒的时间

"""
