$(document).ready(function() {

    $('#like').click(function(){
        $.ajax({
            type: "POST",
            url: "{% url 'song:like_song' %}",
            data: {'slug': $(this).attr('title'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: "json",
            success: function(response) {
                    alert(response.message);
            },
            error: function(rs, e) {
                    alert(rs.responseText);
            }
        });
        })

    });
