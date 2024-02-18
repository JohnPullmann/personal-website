// Select the .menu-bar-btn, .navigation, and .content elements
var menuBarButton = document.querySelector('.menu-bar-btn');
var navigation = document.querySelector('.navigation');
var content = document.querySelector('.content');

// Add a click event listener to the .menu-bar-btn element
menuBarButton.addEventListener('click', function(event) {
    // Prevent the default action of the click event (which is to navigate to the href attribute of the <a> tag)
    event.preventDefault();

    // Toggle the nav-active class on the .menu-bar-btn, .navigation, and .content elements
    this.classList.toggle('nav-active');
    navigation.classList.toggle('nav-active');
    content.classList.toggle('nav-active');
});


// Portfolio Timeline scrolling
$(document).ready(function(){
    $(".timeline-arrow-right").click(function(){
      $(".timeline-cover").animate({scrollLeft: '+=275'}, 800);
    });
    $(".timeline-arrow-left").click(function(){
      $(".timeline-cover").animate({scrollLeft: '-=275'}, 800);
    });
});
$(document).ready(function(){
    $(".timeline-cover").animate({scrollLeft: $(".timeline-cover").prop('scrollWidth')}, 1500);
});