/**
 * Created by munis on 4/12/17.
 */
/*!
 * project-name
 * http://example.url/
 * @author Labrin
 * @author-url http://labrin.net/
 * @version 0.1.0
 * @updated 2017-02-03 */
(function(){$(function(){return console.log("hello world!")})}).call(this),$(function(){if($(".section-underconstruction").length){var a=$("body").height();$(".section-underconstruction").css("height",a),$(window).resize(function(){$(".section-underconstruction").css("height",a)})}var b=new Date,c=new Date(2017,1,1),d=new Date(2017,1,20),e=Math.round(b.getTime()/1e3),f=Math.round(c.getTime()/1e3),g=Math.round(d.getTime()/1e3),h=g-e,i=g-f;$(".progress-bar").attr("aria-valuemax",i);var j=100-Math.round(100*h/i);$(".progress-bar").animate({width:j+"%"},1e3),$("#videoblock").vide("/static/video/video.mp4",{volume:1,playbackRate:1,muted:!0,loop:!0,autoplay:!0,position:"50% 50%",posterType:"detect",resizing:!0,bgColor:"transparent",className:""})});