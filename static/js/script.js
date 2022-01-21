$(document).ready(function () {
    // Toggle navigation
    $("#nav-toggle").click(function () {
        arrowToggle();
        $("#nav-collapse").toggle(500);
    });

    // Bootstrap class control
    loginClassAdd();
    signupClassAdd();
});

/** Check current status of arrow nav toggler and change it to the opposite.*/
function arrowToggle() {
    if ($("#toggle-icon").hasClass("fa-arrow-circle-right")) {
        $("#toggle-icon")
            .removeClass("fa-arrow-circle-right")
            .addClass("fa-arrow-circle-left");
    } else {
        $("#toggle-icon")
            .removeClass("fa-arrow-circle-left")
            .addClass("fa-arrow-circle-right");
    }
}

/** Add Bootstrap classes to Login page inputs dynamically created by allauth */
function loginClassAdd() {
    $("#id_login").addClass("form-control");
    $("#id_password").addClass("form-control");
}

/** Add Bootstrap classes to Signup page inputs dynamically created by allauth */
function signupClassAdd() {
    $("#id_username").addClass("form-control");
    $("#id_email").addClass("form-control");
    $("#id_password1").addClass("form-control");
    $("#id_password2").addClass("form-control");
}
