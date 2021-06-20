function initializeTable() {
    $(document).ready( function () {
        $('#transactionsTable').DataTable(
            {
                "order": [[ 4, "desc" ]],
                "iDisplayLength": 25,
                "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]]
            }
        );
    } );
}

function setEnvironmentSwitch() {
    let envSwitch = document.getElementById("environment-switch");
    envSwitch.checked = envSwitch.dataset.checked == "True";
}

function onEnvironmentSwitchClick() {
    // check if checkbox is checked or not then send to route
    startLoading();
    let checked = document.getElementById("environment-switch").checked;
    window.location = "/update-data-environment?checked=" + checked;
}

function setCurrentTransactionId(tId) {
    sessionStorage["currentTransactionId"] = tId;
}

function getCurrentTransactionId() {
    return sessionStorage["currentTransactionId"]
}

function onTransactionDeleteClick() {
    // delete transaction
    startLoading();
    window.location = "delete-transaction?tId=" + getCurrentTransactionId();
}

function onTransactionOpenClick(tId) {
    setCurrentTransactionId(tId);
    onTransactionClick();
    // update submit button to say "update"
    document.getElementById("submit-button").innerHTML = "Update";
    // populate transaction form with appropriate values
    document.getElementById("amount-input").value = document.getElementById("transaction-amount-" + tId).dataset.value;
    let category = document.getElementById("transaction-category-" + tId).innerHTML
    document.getElementById("category-button").innerHTML = category;
    // set dropdown to be selected
    document.getElementById(category).classList.add("active");
    if(document.getElementById("transaction-isIncome-" + tId).innerHTML == "True") {
        document.getElementById("flexSwitchCheckDefault").checked = "True";
    }
    document.getElementById("note").value = document.getElementById("transaction-note-" + tId).innerHTML;
    document.getElementById("date-input").value = document.getElementById("transaction-date-" + tId).innerHTML;
    // make submit button clickable
    document.getElementById("submit-button").classList.remove("disabled");
    document.getElementById("delete-button").style.display = "inline-block";
}

function submitDate(year, month) {
    // if year is null, then year is whatever is in the year button
    // if month is null, we want to send no month since the new year should have the default first month
    startLoading();
    let url = "/"
    if(year) {
        //only year was given
        url = url + "?selected_year=" + year
    } else {
        // only month was given
        let yearButtonValue = document.getElementById("select_year_button").value;
        url = url + "?selected_year=" + document.getElementById("select_year_button").value + "&selected_month=" + month;
    }
    window.location = url;
}

function onCategorySaveButtonClick(yearId, monthNum, categories) {
    // saves changes made to category input fields [income and banks]
    // first, make a map that maps category name to the budget amount
    startLoading();
    categoryBudgetMap = {};
    for(i=0; i<categories.length; i++) {
        let category = categories[i]
        categoryBudgetMap[categories[i]] = document.getElementById("bank-budget-" + category).value;
    }
    // get income
    let income = document.getElementById("income-input").value;
    // build data object
    const data = {"yId": yearId, "monthNum": monthNum, "banks": categoryBudgetMap, "income": income};
    // send POST request
    let fetchPromise = post("/update-banks-and-income", data);
    fetchPromise.then(response => {
      window.location.href = response.url;
    });
}

function setTotalAmountSpentAndDifference() {
    // get all bank values and sum them up
    // get all bankCategories
    bankCategories = document.getElementsByClassName("bank-category");
    totalBankAmounts = 0;
    totalBudgetAmounts = 0;
    for(i=0; i<bankCategories.length; i++) {
        let category = bankCategories[i].innerHTML;
        totalBankAmounts += parseInt(document.getElementById("bank-amount-spent-" + category).dataset.value);
        totalBudgetAmounts += parseInt(document.getElementById("bank-budget-" + category).value);
    }
    // get income amount
    let income = parseInt(document.getElementById("income-input").value);
    // set amount spent
    document.getElementById("amount-spent").innerHTML = "TOTAL SPENT: $" + totalBankAmounts.toString() + ".00";
    document.getElementById("amount-spent").dataset.value = totalBankAmounts;
    // set difference
    document.getElementById("income-difference").innerHTML = "TOTAL REMAINING: $" + (income - totalBankAmounts).toString() + ".00";
    document.getElementById("income-difference").dataset.value = income - totalBankAmounts;
    // set total budgeted amount
    document.getElementById("amount-budgeted").innerHTML = "TOTAL BUDGETED: $" + totalBudgetAmounts.toString() + ".00";
    document.getElementById("amount-budgeted").dataset.value = totalBudgetAmounts;
}

function init() {
    // calls all methods that need to be run on page load
    initializeTable();
    setEnvironmentSwitch();
    setTotalAmountSpentAndDifference();
}