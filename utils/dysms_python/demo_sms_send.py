# -*- coding: utf-8 -*-
import json
import sys
from importlib import reload
from string import printable

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
# import const
from random import choice

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""
if sys.version_info.major == 2:
    #下面的try是用来设置python2编码的
    try:
        reload(sys)
        sys.setdefaultencoding('utf8')
    except NameError:
        pass
    except Exception as err:
        raise err

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

#直接把const.py里的内容直接考过来
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = "LTAIPJZY3plmWIks"
ACCESS_KEY_SECRET = "dGZGnJEIleNWmNHPQZqPkSaTWS9LVd"

# acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

def send_sms(phone_numbers,code):
    business_id = uuid.uuid1()
    sign_name = "马浩浩"
    template_code = 'SMS_138079053'
    print('短信验证码:',code)
    template_param = json.dumps({"code":code})


    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)

    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)

    # 短信签名
    smsRequest.set_SignName(sign_name)
	
    # 数据提交方式
	# smsRequest.set_method(MT.POST)
	
	# 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
	
    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理


    return smsResponse



# if __name__ == '__main__':
#     __business_id = uuid.uuid1()
#     #print(__business_id)
#     # params = "{\"code\":\"12345\",\"product\":\"云通信\"}"
#     params = {
#         'code':1234
#     }
# 	#params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
#     print(send_sms(__business_id, "133131393592", "马浩浩", "SMS_138079053", json.dumps(params)).decode('utf-8'))
#     print(send_sms('13683153665').decode('utf-8'))
    
    

