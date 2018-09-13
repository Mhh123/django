// 点击发送图形验证码
$(function () {
    var imgCaptcha = $('.img-captcha');
    imgCaptcha.click(function () {
        // 如何实现点击一次图片，刷新一次验证码呢？
        // 在这里利用img的src特点，只要你修改了一次src,img就会重新加载
        imgCaptcha.attr("src", '/account/img_captcha' + "?random=" + Math.random());
    });
});

// $(function(){});相当于window.onload=function(){}
//等到页面加载完再执行function

// 点击发送短信验证码
$(function () {
    var smsCaptcha = $('.sms-captcha-btn');
    smsCaptcha.click(send_sms);


    function send_sms() {
        var telephone = $("input[name='telephone']").val();
        console.log(telephone);
        $.get({
            'url': '/account/sms_captcha/',
            'data': {'telephone': telephone},
            'success': function (res) {
                var count = 60;
                //设置不能点击
                //给span标签添加class
                smsCaptcha.addClass('disabled');
                //移除span标签点击事件
                smsCaptcha.unbind('click');

                var timer = setInterval(function () {
                    smsCaptcha.text(count);
                    count--;
                    if (count <= 0) {
                        smsCaptcha.bind("click", send_sms);
                        smsCaptcha.removeClass('disabled');
                        clearInterval(timer);
                        smsCaptcha.text('发送验证码');

                    }
                }, 1000);
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    }
});


注册功能
// $(function () {
//     var telephoneInput = $("input[name='telephone']");
//     var usernameInput = $("input[name='username']");
//     var img_captchaInput = $("input[name='img_captcha']");
//     var passwordInput = $("input[name='password']");
//     var password1Input = $("input[name='password1']");
//     var sms_captchaInput = $("input[name='sms_captcha']");
//     var submitBtn = $(".submit-btn");
//     submitBtn.click(function () {
//         //阻止默认行为
//         event.preventDefault();
//
//
//         var telephone = telephoneInput.val();
//         var username = usernameInput.val();
//         var img_captcha = img_captchaInput.val();
//         var passowrd = passwordInput.val();
//         var passowrd1 = password1Input.val();
//         var sms_captcha = sms_captchaInput.val();
//
//     });
//
// });