;$(function(){
    $("form").on("submit", function(event){
        event.preventDefault();
        var data = $(this).serialize();
        $.post("#", data, function(res){
            if(res.code != 1){
                swal(
                    res.message,
                    '',
                    'warning'
                );
                return;
            }
            window.location.href = "/";
        },'json');
    });
});