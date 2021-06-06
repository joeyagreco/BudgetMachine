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

function updateCategoryDropdown(category) {
    // remove all 'active' classes from elements in the category dropdown
    let activeElements = document.getElementsByClassName("active");
    for(i=0; i<activeElements.length; i++) {
        // check if this element has the class 'category-item' in its classlist
        if(activeElements[i].classList.contains("category-item")) {
            // then we want to remove the 'active' class
            activeElements[i].classList.remove("active");
        }
    }
    document.getElementById(category).classList.add("active");
    // update button text
    let button =  document.getElementById("category-button")
    button.value = category;
    button.innerText = category;
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
    }
}