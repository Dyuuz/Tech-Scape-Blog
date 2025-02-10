// Nope. CSS is powerful.
function termsclose() {
    var termsbody = document.querySelector(".modal");
    termsbody.style.display = "none";   
}

function termsopen() {
    var termsbody = document.querySelector(".modal");
    termsbody.style.display = "flex";   
}

function declinecheckbox() {
    var termsbody = document.querySelector(".modal");
    var checkbox = document.querySelector("#signup-terms");
    checkbox.checked = false;
    termsbody.style.display = "none";
}
function acceptcheckbox() {
    var termsbody = document.querySelector(".modal");
    var checkbox = document.querySelector("#signup-terms");
    checkbox.checked = true;
    termsbody.style.display = "none";
}
