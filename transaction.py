from app import db


def produce_product(productid, userid):
    product = db.session.execute(
        "SELECT products.itemid, products.shopid FROM products, shop_owners WHERE shop_owners.userid = :userid AND shop_owners.shopid = products.shopid AND products.id = :productid",
        {"productid":productid,"userid":userid}).fetchone()
    if product == None:
        return 403
    itemid, shopid = product
    db.session.execute("UPDATE shop_inventory SET quantity = quantity + 1 WHERE shopid = :shopid AND itemid = :itemid",
        {"shopid":shopid,"itemid":itemid})
    db.session.commit()
    return 200


def do_transaction(productid, userid):
    product = db.session.execute( 
        """SELECT products.shopid, products.itemid, products.price, shop_inventory.quantity 
        FROM products, shop_inventory 
        WHERE products.id = :productid AND shop_inventory.shopid = products.shopid AND shop_inventory.itemid = products.itemid""",
        {"productid":productid}).fetchone()

    if product == None:
        return 404
    shopid, itemid, price, quantity = product
    if quantity < 1: 
        return 404

    buyer_balance = db.session.execute("SELECT balance FROM users WHERE id = :id",{"id":userid}).fetchone()[0]
    if buyer_balance < price:
        return 403 # cannot afford

    db.session.execute("UPDATE shop_inventory SET quantity = quantity - 1 WHERE shopid = :shopid AND itemid = :itemid",
        {"shopid":shopid,"itemid":itemid})

    inventory_entry = db.session.execute("SELECT userid FROM user_inventory WHERE userid = :userid AND itemid = :itemid",{"userid":userid,"itemid":itemid}).fetchone()
    if inventory_entry == None:
        db.session.execute("INSERT INTO user_inventory (userid, itemid, quantity) VALUES (:userid, :itemid, 1)", {"userid":userid,"itemid":itemid})
    else:
        db.session.execute("UPDATE user_inventory SET quantity = quantity + 1 WHERE userid = :userid AND itemid = :itemid",
            {"userid":userid,"itemid":itemid})

    b = db.session.execute("UPDATE users SET balance = balance - 1.0 WHERE id = :userid RETURNING balance", {"price":float(price),"userid":userid}).fetchone()
    b = db.session.execute(
        """UPDATE users SET balance = balance + 
        :price / (SELECT COUNT(users.id) FROM users, shop_owners WHERE shop_owners.userid = users.id AND shop_owners.shopid = :shopid)
        FROM shop_owners WHERE shop_owners.userid = :userid AND shop_owners.shopid = :shopid RETURNING balance""",
        {"shopid":shopid, "price":float(price), "userid":userid}).fetchall()

    db.session.execute(
        """INSERT INTO transactions (shopid, userid, itemid, amount, price, closetime) VALUES (:shopid, :userid, :itemid, 1, :price, NOW())""",
        {"shopid":shopid, "userid":userid, "itemid": itemid, "price":float(price)})
    db.session.commit()
    return 200


def get_transaction_activity(userid):
    purchases = db.session.execute("""
        SELECT items.itemname, shops.shopname, transactions.price, transactions.closetime FROM transactions, items, shops
        WHERE transactions.userid = :userid AND items.id = transactions.itemid 
        AND transactions.shopid = shops.id""", {"userid":userid}).fetchall()
    sales = db.session.execute("""
        SELECT items.itemname, shops.shopname, transactions.price, transactions.closetime, transactions.price / shops.n_owners
        FROM transactions, items, shops, shop_owners
        WHERE transactions.shopid = shops.id AND shop_owners.shopid = shops.id AND shop_owners.userid = :userid AND items.id = transactions.itemid
    """, {"userid":userid}).fetchall()
    activity = [
        {
            "message": f"Bought {itemname} at {shopname} for {price}",
            "date": closetime,
            "payment": -price
        }
        for itemname, shopname, price, closetime in purchases
    ] + [
        {
            "message": f"{shopname} sold {itemname} for {price}",
            "date": closetime,
            "payment": int(payment)
        }
        for itemname, shopname, price, closetime, payment in sales
    ]
    activity.sort(reverse=True, key=lambda a: a["date"])
    return activity[:10]
