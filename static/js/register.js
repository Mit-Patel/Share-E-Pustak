// var data_array="";

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function toJSONString( form ) {
    var obj = {};
    var elements = form.querySelectorAll( "input, select" );
    for( var i = 0; i < elements.length; ++i ) {
        var element = elements[i];
        var name = element.name;
        var value = element.value;

        if( name ) {
            obj[ name ] = value;
        }
    }

    return JSON.stringify( obj );
}

var success_alert="<div class='alert alert-success' role='alert'>Thankyou for registering with us. We have sent you an activation mail. Please activate your account.</div>";

$(document).ready(function(){
    $("#form_register").submit(function(e){
        var data_array = new FormData(this);
        //toJSONString(this);        
        //alert(data_array);
        //    return;    
        e.preventDefault();
        var mob_no = $("#id_mobile_no").val();
        $.ajaxSetup({
            headers:{"X-CSRFToken":getCookie("csrftoken")}
        });
        $.ajax({
            url:'/auth/send_otp/',
            type:'post',
            // data:{"mob_no":mob_no},
            data:data_array,
            processData: false,
            contentType: false,
            cache:false,
            success:function(data){
                $("#modal_register").fadeIn();
                console.log(data)
            }
        })
    });

    $("#form_verify_otp").submit(function(e){
        e.preventDefault();
        
        // var error_alert=;
        var data_array = new FormData($("#form_register")[0]);
        // console.log($("#form_register"));
        var otp = $("#otp").val();
        $.ajaxSetup({
            headers:{"X-CSRFToken":getCookie("csrftoken")}
        });
        $.ajax({
            url:'/auth/verify_otp/',
            type:'post',
            data:{"otp":otp},
            success:function(data){
                console.log("Verification done");
                $("#modal_register").fadeOut();
                $.ajax({
                    url:'/auth/register/',
                    type:'post',
                    data:data_array,
                    processData: false,
                    contentType: false,
                    cache:false,
                    success:function(data){
                        console.log(data.status)
                        // data = JSON.parse(data);
                        if(data.status=="success"){
                            $("#alertDiv").html(success_alert);
                        }
                        else{
                            $("#alertDiv").html("<div class='alert alert-danger' role='alert'>"+data.message+"</div>");
                        }   
                    }
                })
            }
        })
    });
});

$("#id_username").focusout(function () {
    var username = $(this).val();
    
    $.ajax({
      url: '/auth/validate_username/',
      data: {
        'username': username
      },
      dataType: 'json',
      success: function (data) {
        if (data.is_taken) {
          alert(data.error_message);
          $("#id_username").val('');
        }
      }
    });

  });