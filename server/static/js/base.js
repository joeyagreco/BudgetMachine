function reloadPage() {
    location.reload();
}

function leagueHomepageRedirect() {
    var leagueId = document.getElementById("league_id").value;
    startLoading();
    window.location = "/league-homepage?league_id=" + leagueId;
}

function statExplanationRedirect() {
    var leagueId = document.getElementById("league_id").value;
    startLoading();
    window.location = "/stats-explained?league_id=" + leagueId;
}

function aboutRedirect() {
    var leagueId = document.getElementById("league_id").value;
    startLoading();
    window.location = "/about?league_id=" + leagueId;
}

function feedbackRedirect() {
    var leagueId = document.getElementById("league_id").value;
    startLoading();
    window.location = "/feedback?league_id=" + leagueId;
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

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
    }
}