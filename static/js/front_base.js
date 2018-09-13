$(function () {
    if(window.template){
        template.defaults.imports.timeSince = function (dateValue) {
        var date = new Date(dateValue); //都是毫秒/秒，相差1000倍
        var datets = date.getTime();
        var nows = (new Date()).getTime();
        var timestamp = (nows-datets) / 1000;

        if (timestamp < 60) {
            return '刚刚';
        }
        else if (timestamp >= 60 && timestamp < 60 * 60) {
            var minutes = parseInt(timestamp / 60);
            return minutes + '分钟前';
        }
        else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
            var hours = parseInt(timestamp / 60 / 60);
            return hours + '小时前';
        }
        else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
            var days = parseInt(timestamp / 60 / 60 / 24);
            return days + '天前';
        }
        else {
            // "%Y/%m/%d %H:%M"
            var year = date.getFullYear();
            var month = date.getMonth();
            var day = date.getDay();
            var hour = date.getHours();
            var minute = date.getMinutes();
            return year + '/' + month + '/' + day + ' ' + hour + ':' + minute;
        }
    };
    }
});