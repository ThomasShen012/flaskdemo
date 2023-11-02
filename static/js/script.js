$("form[name=signup_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/user/login";
            window.alert("註冊成功");
        },
        
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }

    });
    e.preventDefault();

});

$("form[name=login_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/";
            window.alert("登入成功");
        },
        error: function(resp) {
            console.log(resp);
            /*window.alert(resp.responseJSON.error);*/
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }

    });
    e.preventDefault();

});

$("form[name=update_user_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/update_user",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/memberprofile";
            window.alert("User update");
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }

    });
    e.preventDefault();

});

$("#password, #password_confirm").on("keyup", function () {
    $(".confirm-message")
        .removeClass("success-message")
        .removeClass("error-message");

    let password = $("#password").val();
    let confirm_password = $("#password_confirm").val();

    if (confirm_password === "") {
        $(".confirm-message")
            .text("Confirm Password Field cannot be empty")
            .addClass("error-message");
    } else if (confirm_password === password) {
        $(".confirm-message")
            .text("Password Match!")
            .addClass("success-message");
    } else {
        $(".confirm-message")
            .text("Password Doesn't Match!")
            .addClass("error-message");
    }
});

$("form[name=add_event_form]").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/add_event",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/eventlist";
            window.alert("Event added");
        },
        error: function (resp) {
            console.log("script: failed" + resp.responseJSON.error);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        },
    });
    e.preventDefault();
});

$("form[name=update_event_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    /*console.log(event_title);*/
    
    $.ajax({
        url: "/update_event/" + event_title, 
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            window.location.href = "/eventlist";
            window.alert("Event updated");
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }

    });
    e.preventDefault();

});