var scrolled = 0;

$(document).ready(function () {


    $("#downClick").on("click", function () {

        $(".scroll-area").animate({
            scrollTop: 9999999
        });

    });


    $("#upClick").on("click", function () {
        scrolled = scrolled - 300;

        $(".scroll-area").animate({
            scrollTop: scrolled
        });

    });


});

