function checkProduct(shop_products) {
    const productValidationMessage = document.getElementById("productValidationMessage")
    const selectInput = document.getElementById("productItemSelect")
    const priceInput = document.getElementById("productPrice")
    const submitButton = document.getElementById("productSubmit")

    const price = priceInput.value
    const itemname = selectInput.value

    const [valid, message] = (() => {
        if (itemname == "") {
            return [false, "Please select an item"]
        }
        const item_already_for_sale = shop_products.some((item) => 
            item == itemname
        )
        if (item_already_for_sale) {
            return [false, "Item is already listed in this shop"]
        }
        if (isNaN(price) || price.trim() == "") {
            return [false, "Price must be a number"]
        }
        return [true, "Ok"]
    })()

    if (!valid) {
        productValidationMessage.innerHTML = message
        submitButton.classList.add("disabled")
        selectInput.classList.add("outline-danger")
        priceInput.classList.add("outline-danger")
    } else {
        productValidationMessage.innerHTML = ""
        submitButton.classList.remove("disabled")
        selectInput.classList.remove("outline-danger")
        priceInput.classList.remove("outline-danger")
    }

    return valid
}