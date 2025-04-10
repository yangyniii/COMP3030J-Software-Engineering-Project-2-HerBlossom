;(function ($) {
    "use strict";

    /*============= preloader js_test css_test =============*/
    var cites = [];
    cites[0] = "Empowering Every Queen, One Click at a Time";
    cites[1] = "Where Every Woman Finds Her Voice, Power, and Path";
    cites[2] = "Power in Unity, Strength in Support";
    cites[3] = "Digital Strength for Real Queens";
    var cite = cites[Math.floor(Math.random() * cites.length)];
    $('#preloader p').text(cite);
    $('#preloader').addClass('loading');

    $(window).on( 'load', function() {
        setTimeout(function () {
            $('#preloader').fadeOut(500, function () {
                $('#preloader').removeClass('loading');
            });
        }, 500);
    })

})(jQuery)