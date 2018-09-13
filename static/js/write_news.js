

// $(function(){
//     var $uploadBtn = $("#upload-btn");
//
//     // 监听change事件
//     $uploadBtn.change(function(){
//         event.preventDefault();
//         var file = this.files[0];
//         var formdata = new FormData();
//         formdata.append('upfile',file);
//
//         xfzajax.post({
//             'url':'/cms/upload_file/',
//             'data':formdata,
//             'processData':false,
//             'contentType':false,
//             'success':function(result){
//                 if (result['code'] == 200){
//                     var url = result['data']['url'];
//                     var $thumbnailInput = $("input[name='thumbnail']");
//                     $thumbnailInput.val(url);
//                 }
//             }
//         });
//     });
// });


// 上传文件到七牛云
$(function () {
    function progess(response) {
        // console.log(response);
        //total : {loaded: 30038, size: 30038, percent: 100}
        var percent = response.total.percent;
    }

    function error(err) {
        window.messageBox.showError(err.message);
    }

    function complete(response) {
        // console.log(response);
        //{hash: "Fgch7c-Fyy4ASVO81O0aG3LJFxAe", key: "圆通.PNG"}
        // hash key
        var key = response.key;
        var domain = 'http://p7bj6aatj.bkt.clouddn.com/';
        var url = domain + key;
        var $thumbnailInput = $("input[name='thumbnail']");
        $thumbnailInput.val(url);
    }

    var $uploadBtn = $("#upload-btn");
    $uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] == 200) {
                    var token = result['data']['token'];
                    var key = file.name;
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpeg',
                            'image/gif'] || null
                    };
                    var config = {
                        useCdnDomain: true,
                        region: qiniu.region.z0
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        'next': progess,
                        'error': error,
                        'complete': complete
                    });
                }
            }
        });
    });
});


//实例化编辑器
$(function () {
    //将ue变成一个全局的变量 window.ue
    window.ue = UE.getEditor('editor',{
        initialFrameHeight:400,
        serverUrl:'/ueditor/upload/'
    });
});


$(function () {
    var $submitBtn = $("#submit-btn");
    $submitBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var desc = $("input[name='desc']").val();
        var category = $("select[name='category']").val();
        var thumbnail = $("input[name='thumbnail']").val();

        var content = window.ue.getContent();

        xfzajax.post({
            'url':'/cms/write_news/',
            'data':{
                'title':title,
                'desc':desc,
                'category':category,
                'thumbnail':thumbnail,
                'content':content
            },
            'success':function(result){
                if (result['code'] == 200) {
                    xfzalert.alertSuccess('恭喜!新闻发表成功',function () {
                        window.location.reload();
                    })
                }
            }
        });
    });
});