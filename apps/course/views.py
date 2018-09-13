import time

import hashlib
import hmac
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from utils import restful

from .models import Course, CourseOrder


# Create your views here.


def course_index(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    context = {
        'course': course,
    }
    return render(request, 'course/course_detail.html', context=context)


def course_token(request):
    video_url = request.GET.get('video_url')
    course_id = request.GET.get('course_id')

    buyed = CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists()
    if not buyed:
        return restful.params_error(message="请先购买课程!")

    # video_url=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    expriation_time = int(time.time()) + 2 * 60 * 60
    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(video_url)[1]
    media_id = video_url.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expriation_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expriation_time)
    return restful.result(data={'token': token})


def course_order(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(pk=course_id)
    buyed = CourseOrder.objects.filter(buyer=request.user, course=course, status=2).exists()
    if buyed:
        return redirect(reverse("course:course_detail", kwargs={
            "course_id": course.pk
        }))
    order = CourseOrder.objects.create(amount=course.price, course=course,
                                       buyer=request.user, status=1)
    context = {
        'course': course,
        'notify_url': request.build_absolute_uri(reverse('course:notify_url')),
        'return_url': request.build_absolute_uri(reverse(
            'course:course_detail', kwargs={"course_id": course.pk})),
        'order': order
    }

    return render(request, 'course/create_order.html', context=context)


def order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = 'e6110f92abcb11040ba153967847b7a6'
    orderuid = str(request.user.pk)
    uid = '49dc532695baa99e16e01bc0'

    key = hashlib.md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url
                       + token + uid).encode("utf-8")).hexdigest()
    # key = hashlib.md5(
    #     "".join([goodsname, istype, notify_url, orderid, orderuid, price, return_url, token, uid]).encode(
    #         "utf-8")).hexdigest()
    return restful.result(data={'key': key})


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
