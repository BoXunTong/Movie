//		轮播效果js
var index = 0;

var list = $('.list li');

var btn = $('.btn li');

var arrow = $('.arrow');

function demo(num) {

    list.eq(num).stop().fadeIn().siblings().stop().fadeOut();

    btn.eq(num).addClass('on').siblings().removeClass('on');

}


btn.click(function() {

    demo(index = $(this).index());

});


arrow.eq(0).click(function() {

    index--;

    index = index < 0 ? list.length - 1 : index;

    demo(index);

});

arrow.eq(1).click(function() {

    index++;

    index = index > list.length - 1 ? 0 : index;

    demo(index);

});

var sid = setInterval(play, 3000);

function play() {

    index++;

    index = index > list.length - 1 ? 0 : index;

    demo(index);

};

$('.banner').hover(function() {
    clearInterval(sid);
}, function() {
    sid = setInterval(play, 3000);
});