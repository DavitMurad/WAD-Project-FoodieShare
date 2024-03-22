function performSearch() {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();
    const posts = document.querySelectorAll('.post');

    posts.forEach(post => {
        const username = post.getAttribute('data-username').toLowerCase();
        const recipe = post.getAttribute('data-recipe').toLowerCase();
        
        if (username.includes(searchTerm) || recipe.includes(searchTerm)) {
            post.style.display = ''; 
        } else {
            post.style.display = 'none'; 
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");

    searchInput.addEventListener('input', performSearch);
    searchButton.addEventListener('click', performSearch);
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-comments').forEach(button => {
        button.addEventListener('click', function() {
            const commentsContainer = this.nextElementSibling;
            commentsContainer.style.display = commentsContainer.style.display === 'none' ? '' : 'none';
        });
    });
});

$('.post').hover(
    function() { // Mouse over
        $(this).css({
            'border-color': '#ffa726',
            'box-shadow': '0 2px 5px rgba(0,0,0,0.2)'
        });
    },
    function() { // Mouse out
        $(this).css({
            'border-color': '#ddd',
            'box-shadow': 'none'
        });
    }
);


$(document).ready(function(){
    var hoverTimeout;
    $('.post').hover(
        function() {
            // Mouse over
            var postElement = $(this); 
            postElement.css({
                'border-color': '#ffa726',
                'box-shadow': '0 2px 5px rgba(0,0,0,0.2)'
            });
            hoverTimeout = setTimeout(function() {
                showNotification("This looks delicious, press to see how to prepare this dish at home!", postElement);
            }, 3000); 
        }, 
        function() {
            // Mouse out
            var postElement = $(this);
            // Revert styles
            postElement.css({
                'border-color': '#ddd',
                'box-shadow': 'none'
            });
            clearTimeout(hoverTimeout);
            $('#notification').stop(true).fadeOut(200); // hide the notification 
        }
    );

    function showNotification(message, postElement) {
        var notification = $('#notification');
        notification.text(message).fadeIn(200).off("click").on("click", function() {
            window.location.href = postElement.data('recipe-url');
            $(this).fadeOut(200);
        });
    }
});
