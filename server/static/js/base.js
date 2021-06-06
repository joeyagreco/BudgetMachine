function reloadPage() {
    location.reload();
}

function startLoading() {
    document.querySelector("#loader-wrapper").style.display = "flex";
    document.querySelector("#loader-wrapper").style.visibility = "visible";
}

function stopLoading() {
    document.querySelector("#loader-wrapper").style.display = "none";
    document.querySelector("#loader-wrapper").style.visibility = "hidden";
    document.querySelector("body").style.visibility = "visible";
}

function onTransactionClick() {
    document.getElementById("transaction-form").style.display = "flex";
    document.getElementById("form-background").style.display = "block";
}

function onTransactionCloseClick() {
    document.getElementById("transaction-form").style.display = "none";
    document.getElementById("form-background").style.display = "none";
}

function onTransactionSubmitClick() {
    document.getElementById("transaction-form").style.display = "none";
    document.getElementById("form-background").style.display = "none";
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
        $('.datepicker').datepicker();
    } else {
        stopLoading();
    }
}