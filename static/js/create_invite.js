function checkInvite(owners) {
    submit = document.getElementById("inviteSubmit")
    receiver = document.getElementById("receivername").value
    if (receiver == "" || owners.includes(receiver)) {
        submit.classList.add("disabled")
    } else {
        submit.classList.remove("disabled")
    }
}