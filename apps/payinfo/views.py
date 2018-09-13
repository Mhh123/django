from django.shortcuts import render

# Create your views here.


def pay_info(request):
    return render(request,'payinfo/payinfo.html')