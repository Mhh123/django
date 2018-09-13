#encoding:utf-8

class FormMixin(object):
    def get_error(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            error_tuple = errors.popitem()
            error_list = error_tuple[1]
            error_dict = error_list[0]
            message = error_dict['message']
            return message
        else:
            return None

            # print(type(form.errors))
            #<class 'django.forms.utils.ErrorDict'>
            # print(form.errors.get_json_data())
            # {'password': [{'code': 'required', 'message': '必须输入密码!'}],
            #  'sms_captcha': [{'code': 'required', 'message': '这个字段是必填项。'}],
            #  'password1': [{'code': 'required', 'message': '必须输入密码!'}],
            #  'img_captcha': [{'code': 'required', 'message': '这个 字段是必填项。'}],
            #  'username': [{'code': 'required', 'message': '这个字段是必填项。'}],
            #  'telephone': [{'code': 'required', 'message': '必须输入手机号码!'}]}
            # error_dicts = form.errors.get_json_data()
            # error_tuple = error_dicts.popitem()
            # print(error_tuple)
            #('img_captcha', [{'code': 'required', 'message': '这个字段是必填项。'}])
            # error_list = error_tuple[1]
            # print(error_list)
            #[{'message': '必须输入密码!', 'code': 'required'}]
            # error_direct = error_list[0]
            # messages = error_direct['message']
            # print(messages)
            #必须输入密码!