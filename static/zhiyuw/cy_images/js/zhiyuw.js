var zhiyuw = {};
(function(parent, $){
    var _bindLoginSlide = function () {
        $('#test2_li_now_ li').click(function(){
            $(this).parent().find('li').attr('class', '');
            $(this).attr('class', 'now');
        });
     };

    var index = parent.index = function (){
        var _bindEventHandle = function () {
            _bindLoginSlide();
        };
        return {
                init: function () {
                    _bindEventHandle();
                },
        };
    }();

    var login = parent.login = function (){
        var _bindEventHandle = function () {
            _bindLoginSlide();
        };
        return {
                init: function () {
                    _bindEventHandle();
                },
        };
    }();
})(zhiyuw || {}, jQuery);
