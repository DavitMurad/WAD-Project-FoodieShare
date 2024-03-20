$(document).ready(function(){
    $('.navbar-links a', ' .navbar').hover(
        function() {
            // Mouse over
            $(this).animate({
                'font-size': '20px'
            }, 200);
        }, 
        function() {
            // Mouse out
            $(this).animate({
                'font-size': '18px'
            }, 200);
        }
    );
});
