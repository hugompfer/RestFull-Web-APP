$(function () {
    $('#login-tab').click(function (e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-tab').removeClass('active');
        document.getElementById("login-form").reset();
        clearAlerts();
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-tab').click(function (e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        document.getElementById("register-form").reset();
        clearAlerts();
        $('#login-tab').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

});


function loginUser() {
    var form = document.getElementById("login-form");
    var name = form.username.value;
    var password = form.password.value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/user/login/");
    req.setRequestHeader("Content-Type", "application/json");
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        if (response["credentials"]) {
            showWarningMessage(response["credentials"]);
        } else {
            window.location.href = response["redirect"];
        }
    });
    req.send(JSON.stringify({ "username": name, "password": password }));
}


function registerUser() {
    var form = document.getElementById("register-form");
    var name = form.name.value;
    var email = form.email.value;
    var username = form.usernameRegister.value;
    var password = form.passwordRegister.value;

    var req = new XMLHttpRequest();
    req.open("POST", "/api/user/register/");
    req.setRequestHeader("Content-Type", "application/json");
    req.addEventListener("load", function () {
        var response = JSON.parse(this.responseText);
        if (response["username"]) {
            showWarningMessage(response["username"]);
        } else if (response["email"]) {
            showWarningMessage(response["email"]);
        } else if (response["error"]) {
            showDangerMessage(response["error"]);
        }else{
            document.getElementById("login-tab").click();
            showSuccessMessage("Registo efetuado com sucesso");
        }
    });

    req.send(JSON.stringify({ "username": username, "password": password, "name": name, "email": email }));
}
