function deleteMessage(id) {
    $.ajax({
        url: '/messages/' + id,
        type: 'DELETE',
        success: function(result) {
            window.location.href = "/";
        }
    });
}
