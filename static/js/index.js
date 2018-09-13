//加载更多新闻的事件
$(function () {
    var page = 2;
    var $loadBtn = $('.load-more-btn');
    $loadBtn.click(function () {
        var $li = $(".list-tab-group li.active");
        var category_id = $li.attr('data-category-id');
        var page = parseInt($loadBtn.attr("data-page"));
        xfzajax.get({
            'url': '/news/news_list/',
            'data': {
                'p': page,
                'category_id': category_id
            },
            'success': function (result) {
                newses = result['data'];
                if (newses.length > 0) {
                    var tml = template("news-item", {"newses": newses});
                    var $newsList = $(".news-list-group");
                    $newsList.append(tml);
                    page += 1;
                    $loadBtn.attr("data-page", page);
                } else {
                    window.messageBox.showInfo("没有更多数据了。。。", "info");
                }

            }
        });
    });
});


$(function () {
    var $categoryUl = $(".list-tab-group");
    var liTags = $categoryUl.children();
    liTags.click(function(){
        var li = $(this);
        var categoryId = li.attr("data-category-id");
        var loadBtn = $(".load-more-btn");
        xfzajax.get({
            'url': '/news/news_list/',
            'data': {
                'category_id': categoryId
            },
            'success': function(result){
                var newes = result['data'];
                var tml = template("news-item", {"newses": newes});
                var newsListGroup = $(".news-list-group");
                //empty: 可以将newsListGroup下所有的标签都清除掉
                newsListGroup.empty();
                newsListGroup.append(tml);
                li.addClass('active').siblings().removeClass('active');
                loadBtn.attr("data-page", 2);
            }
        });
    });
});