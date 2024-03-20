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

// jQuery to fade in elements on scroll
$(window).scroll(function() {
    $('.fade-in').each(function(){
        var elementTop = $(this).offset().top;
        var windowBottom = $(window).scrollTop() + $(window).height();
        if (elementTop < windowBottom) {
            $(this).animate({ opacity: 1 }, 1500);
        }
    });
});
