$(document).ready(function() {
    $('#signupform input[name=username]').on('input', function(event) {


        $.ajax({
            data: {
                username: $('#signupform input[name=username]').val()
            },
            type: 'POST',
            url: '/username',
            success: function(data) {
                $('#availability').text(data.result);
            }
        });
        event.preventDefault();
    });

});