$(function () {
    $('.tag-slider .sl-all-teg > a').click(function (e) {
        e.preventDefault();
        $('.tag-slider').toggleClass('active');
    });
});