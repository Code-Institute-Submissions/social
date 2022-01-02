$(document).ready(function () {
    /** Toggle navigation */
    $("#nav-toggle").click(function () {
        arrowToggle();
        $("#nav-collapse").toggle(500);
    });
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
