// method for sending POST requests
window.post = function(url, data) {
    return fetch(url, {method: "POST", body: JSON.stringify(data)});
}

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
    document.getElementById("delete-button").style.display = "none";
    setTransactionPopupToDefaultValues();
}

function onTransactionSubmitClick() {
    // get data from html
    const amount = document.getElementById("amount-input").value;
    const note = document.getElementById("note").value;
    const category = document.getElementById("category-button").value;
    const isIncome = document.getElementById("flexSwitchCheckDefault").checked.toString();
    const date = document.getElementById("date-input").value;
    // build data object
    const data = {"amount": amount, "note": note, "category": category, "isIncome": isIncome, "date": date}
    // send POST request
    let fetchPromise = post("/add-transaction", data);
    fetchPromise.then(response => {
      window.location.href = response.url;
    });
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

    // validation for submit button
    activateSubmitButtonIfValidInput();
}

function setTransactionPopupToDefaultValues() {
    // set amount to empty string
    document.getElementById("amount-input").value = "";

    // set category dropdown to "category"
    // and remove any 'active' classes in dropdown
    let activeElements = document.getElementsByClassName("active");
    for(i=0; i<activeElements.length; i++) {
        // check if this element has the class 'category-item' in its classlist
        if(activeElements[i].classList.contains("category-item")) {
            // then we want to remove the 'active' class
            activeElements[i].classList.remove("active");
        }
    }
    // update button text
    let button =  document.getElementById("category-button")
    button.value = "Category";
    button.innerText = "Category";

    // set income to false
    document.getElementById("flexSwitchCheckDefault").checked=false;

    // set note to empty string
    document.getElementById("note").value = "";

    // set date to current date
    let date = new Date()
    let dd = String(date.getDate()).padStart(2, '0');
    let mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = date.getFullYear();
    today = yyyy + "-" + mm + "-" +  dd;
    document.getElementById("date-input").value = today;
}

function activateSubmitButtonIfValidInput() {
    const amount = document.getElementById("amount-input").value.replaceAll(/\s/g,'');
    const category = document.getElementById("category-button").innerText;
    if(amount.length > 0 && category != "Category") {
        document.getElementById("submit-button").classList.remove("disabled");
    }
    else {
        document.getElementById("submit-button").classList.add("disabled");
    }
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
    }
}