function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $('.like-btn').click(function() {
        const postId = $(this).data('post-id');
        const ajaxUrl = $(this).data('ajax-url'); // Read the URL from the data attribute
        const btn = $(this); // Capture the button for use in the callback
        
        $.ajax({
            url: ajaxUrl,
            method: 'POST',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
            },
            success: function(data) {
                console.log(data);  // See what data you're getting back
                btn.text(data.liked ? 'Unlike' : 'Like');
                $(`#like-count-${postId}`).text(`${data.total_likes} Likes`);
            }
            
        });
    });
    
});
