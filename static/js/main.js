$(document).ready(function() {
  "Apollo";

  var windowWidth = $(window).width();
  var windowHeight = $(window).height();
  var headerHeight = $("header").height();
  var fitscreen = windowHeight - headerHeight;

  $(".fullscreen").css("height", windowHeight);
});
