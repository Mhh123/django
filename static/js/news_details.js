$(function () {
    var $submitBtn = $("#submit-comment-btn");
    var $textArea = $("#comment-textarea");
    $submitBtn.click(function (){
        var content = $textArea.val();
        var news_id = $submitBtn.attr("data-news-id");
        xfzajax.post({
            'url': '/news/add_comment/',
            'data': {
                'content': content,
                'news_id': news_id,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var comment = result['data'];
                    var tpl = template("comment-item", {"comment": comment});
                    var $commentGroup = $(".comment-list-group");
                    $commentGroup.prepend(tpl);
                    $textArea.val('');
                }else{
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
});