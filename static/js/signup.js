var usernameValid = false
var passwordValid = false

function checkForm() {
    if (usernameValid && passwordValid) {
        document.getElementById("submit").classList.remove("disabled")
    } else {
        document.getElementById("submit").classList.add("disabled")
    }
}

function checkUsername(usernames) {
    const username = document.getElementById("username").value
    const message = document.getElementById("usernameHelp")

    var valid = false
    if (/\s/.test(username)) {
        message.innerText = "Username cannot contain whitespace"
    } else if (username.length < 1 || username.length > 16) {
        message.innerText = "Username must be between 1 and 16 characters"
    } else if (usernames.includes(username)) {
        message.innerText = "Username taken"
    } else {
        message.innerText = "";
        valid = true
    }

    usernameValid = valid
    checkForm()
}

function checkPassword() {
    const password = document.getElementById("password").value
    const message = document.getElementById("passwordHelp")

    var valid = false
    if (password.length < 1 || password.length > 16) {
        message.innerText = "Password must be between 1 and 16 characters"
    } else {
        message.innerText = ""
        valid = true
    }

    passwordValid = valid
    checkForm()
}