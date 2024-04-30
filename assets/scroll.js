var scrolled = 0;

$(document).ready(function () {


    $("#downClick").on("click", function () {

        $(".msg_table>.mantine-ScrollArea-viewport").animate({
            scrollTop: 9999999
        });

    });


    $("#upClick").on("click", function () {
        scrolled = scrolled - 300;

        $(".msg_table>.mantine-ScrollArea-viewport").animate({
            scrollTop: scrolled
        });

    });


});

