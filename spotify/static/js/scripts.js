$(function () {

    var hover_timer = null;
    function show_profile_popover(e) {
        var $el = $(e.target);

        hover_timer = setTimeout(function () {
            hover_timer = null;
            $.ajax({
                type: 'GET',
                url: $el.data('href'),
                success: function (data) {
                    $el.popover({
                        html: true,
                        content: data,
                        trigger: 'manual',
                        animation: false
                    });
                    $el.popover('show');
                    $('.popover').on('mouseleave', function () {
                        setTimeout(function () {
                            $el.popover('hide');
                        }, 200);
                    });
                }
            });
        }, 500);
    }

    function hide_profile_popover(e) {
        var $el = $(e.target);

        if (hover_timer) {
            clearTimeout(hover_timer);
            hover_timer = null;
        } else {
            setTimeout(function () {
                if (!$('.popover:hover').length) {
                    $el.popover('hide');
                }
            }, 200);
        }
    }

    var resfresh=setInterval(function(){
        $.ajax({
                type: 'GET',
                url: '/ajax/get/orders',
                cache:false,
                datatype: 'html',
                success: function (data) {
                    $('#table').html(data)

                }
            });

    },5000)

    $('.profile-popover').hover(show_profile_popover.bind(this), hide_profile_popover.bind(this));

});
