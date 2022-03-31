$(document).ready(function () {
    var currentLoc = window.location.href;
    $('li.nav-item a').each(function () {
        if (this.href === currentLoc) {
            $(this).addClass("active");
        }
    });
});