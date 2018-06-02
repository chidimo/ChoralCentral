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

var $imgpreview = $('#scorePngPreview');

$('img').on('mouseenter', function() {
    var img = this,
        $img = $(img),
        offset = $img.offset();

    $imgpreview
    .css({
        'top': offset.top,
        'left': offset.left
    })
    .append($img.clone())
    .removeClass('hidden');
});

$imgpreview.on('mouseleave', function() {
    $imgpreview.empty().addClass('hidden');
});
