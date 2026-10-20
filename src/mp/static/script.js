$(document).ready(function () {
    
    $("#register").on("submit", function (e) {
        e.preventDefault();

        const name = $("#fullname").val().trim();
        const email = $("#email").val().trim();
        const password = $("#password").val();
        const confirm = $("#confirm-password").val();

        if (name === "") {
            alert("Введите имя");
            return;
        }
        if (email === "" || !email.includes("@")) {
            alert("Введите корректный email");
            return;
        }
        if (password.length < 6) {
            alert("Пароль должен содержать минимум 6 символов");
            return;
        }
        if (password !== confirm) {
            alert("Пароли не совпадают");
            return;
        }

        const $btn = $(this).find("button[type=submit]");
        $btn.prop("disabled", true);

        $.ajax({
            method: "POST",
            url: "/register",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                name: name,
                email: email,
                password: password   
            })
        })
        .done(function () {
            alert("Регистрация успешна!");
            window.location.href = "/login";
        })
        .fail(function (xhr) {
            alert((xhr.responseJSON && xhr.responseJSON.error) || "Ошибка регистрации");
        })
        .always(function () {
            $btn.prop("disabled", false);
        });
    });

    $("#login-form").on("submit", function (e) {
        e.preventDefault();

        const email = $("#login-email").val().trim();
        const password = $("#login-password").val();

        if (email === "" || password === "") {
            alert("Заполните все поля");
            return;
        }

        const $btn = $(this).find("button[type=submit]");
        $btn.prop("disabled", true);

        $.ajax({
            method: "POST",
            url: "/user_authorization",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                email: email,
                password: password
            })
        })
        .done(function () {
            alert("Вы успешно вошли в систему!");
            window.location.href = "/lk"; 
        })
        .fail(function (xhr) {
            alert((xhr.responseJSON && xhr.responseJSON.error) || "Ошибка авторизации");
        })
        .always(function () {
            $btn.prop("disabled", false);
        });
    });
});