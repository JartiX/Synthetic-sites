
$(document).on('click', ".sl-next", function () {
    var slLinks = $(this).parents('.sl-links');
    right_carusel(slLinks);
    return false;
});

$(document).on('click', ".sl-prev", function () {
    var slLinks = $(this).parents('.sl-links');
    left_carusel(slLinks);
    return false;
});

function left_carusel(slLinks) {
    var slLinks_width = $(slLinks).find('.item').outerWidth();
    $(slLinks).find(".sl-items .item").eq(-1).clone().prependTo($(slLinks).find(".sl-items"));
    $(slLinks).find(".sl-items").css({ "left": "-" + slLinks_width + "px" });
    $(slLinks).find(".sl-items").stop().animate({ left: "0px" }, 200);
    $(slLinks).find(".sl-items .item").eq(-1).remove();
}

function right_carusel(slLinks) {
    var slLinks_width = $(slLinks).find('.item').outerWidth();
    $(slLinks).find(".sl-items").stop().animate({ left: "-" + slLinks_width + "px" }, 200);
    setTimeout(function () {
        $(slLinks).find(".sl-items .item").eq(0).clone().appendTo($(slLinks).find(".sl-items"));
        $(slLinks).find(".sl-items .item").eq(0).remove();
        $(slLinks).find(".sl-items").css({ "left": "0px" });
    }, 300);
}