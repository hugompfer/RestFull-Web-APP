function showDangerMessage(message) {
    var alert = document.getElementById("danger");
    alert.children[1].textContent = message;
    alert.style.display="block";
}

function showSuccessMessage(message) {
    var alert = document.getElementById("success");
    alert.children[1].textContent = message;
    alert.style.display="block";
}

function showWarningMessage(message) {
    var alert = document.getElementById("warning");
    alert.children[1].textContent = message;
    alert.style.display="block";
}

document.getElementById("closeTabDanger").addEventListener("click", function () {
    document.getElementById("closeTabDanger").parentElement.style.display = "none";
});

document.getElementById("closeTabSucess").addEventListener("click", function () {
    document.getElementById("closeTabSucess").parentElement.style.display = "none";
});

document.getElementById("closeTabWarning").addEventListener("click", function () {
    document.getElementById("closeTabWarning").parentElement.style.display = "none";
});

function clearAlerts(){
    document.getElementById("closeTabSucess").parentElement.style.display = "none";
    document.getElementById("closeTabWarning").parentElement.style.display = "none";
    document.getElementById("closeTabDanger").parentElement.style.display = "none";
}