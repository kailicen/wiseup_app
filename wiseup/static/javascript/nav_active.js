$(document).ready(function () {
    var currentLoc = window.location.href;

    if (currentLoc.includes("?search=") === true) {
        currentLoc = currentLoc.substring(0, currentLoc.indexOf("?"));
    }

    $('li.nav-item a').each(function () {
        if (this.href === currentLoc) {
            $(this).addClass("active");
        }
    });
});