function leaveSubmit(n_owners) {
    let action
    console.log("leaving shop :(")
    if (n_owners == 1) {
        action = window.confirm("Are you sure you want to leave this shop? You are the last owner and the shop will become inactive. (This action cannot be undone)")
    } else {
        action = window.confirm("Are you sure you want to leave this shop? If you change your mind, the other owner(s) must invite you.")
    }
    return action
}