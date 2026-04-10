$(document).ready(function(){
    $("#register").on("submit", function(e){
        e.preventDefault();
        err=0;
        if($("#fullname").val().trim()==" "  || $("#password").val()!=$("#confirm-password")){
            err=1
        }else{
            err=0
        }
        $.ajax({
            method: "POST",
            url: "/register",
            connectionType:"application/json",
            data:JSON.stringify({
                name: $("#fullname").val(),
                email: $("#email").val(),
                password: $("#password").val()
            })
        })
            .done(function(){
                alert(123)
            })
    })
});