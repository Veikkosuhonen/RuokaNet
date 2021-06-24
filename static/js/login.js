function checkLogin() {
    if (document.getElementById("username").value && document.getElementById("password").value) {
        document.getElementById("submit").classList.remove("disabled")
    } else {
        document.getElementById("submit").classList.add("disabled")
    }
}