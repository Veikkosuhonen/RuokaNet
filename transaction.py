from app import db
import util
from flask import abort
from error import ErrorMessage

def do_buy_transaction(productid, userid):
    product = db.session.execute( 
        """SELECT products.shopid, products.itemid, products.price, shop_inventory.quantity 
        FROM products, shop_inventory 
        WHERE products.id = :productid AND shop_inventory.shopid = products.shopid AND shop_inventory.itemid = products.itemid""",
        {"productid":productid}).fetchone()

    if product == None:
        abort(404)
    shopid, itemid, price, quantity = product
    next = "/shops/"+str(shopid)
    if quantity < 1: 
        raise ErrorMessage("Product is out of stock", next=next)
    owns_shop = db.session.execute("SELECT * FROM shop_owners WHERE userid = :userid AND shopid = :shopid", {"userid":userid, "shopid":shopid}).fetchone()
    if owns_shop != None:
        raise ErrorMessage("You are not allowed to buy from yourself", next=next)

    buyer_balance = db.session.execute("SELECT balance FROM users WHERE id = :id",{"id":userid}).fetchone()[0]
    if buyer_balance < price:
        raise ErrorMessage(f"You cannot afford that (your wallet balance is {buyer_balance})", next=next)

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
            "date": closetime.strftime("%d/%m/%Y %H:%M:%S"),
            "payment": -price
        }
        for itemname, shopname, price, closetime in purchases
    ] + [
        {
            "message": f"{shopname} sold {itemname} for {price}",
            "date": closetime.strftime("%d/%m/%Y %H:%M:%S"),
            "payment": int(payment)
        }
        for itemname, shopname, price, closetime, payment in sales
    ]
    activity.sort(reverse=True, key=lambda a: a["date"])
    return activity[:10]


def get_transactions(querystring, filter):
    result = db.session.execute("""
        SELECT shops.id, shops.shopname, users.username, items.itemname, transactions.price, transactions.amount, transactions.closetime
        FROM transactions, shops, users, items 
        WHERE transactions.shopid = shops.id AND transactions.userid = users.id AND transactions.itemid = items.id""").fetchall()
    return list(map(
        lambda t: {
            "shopid":t[0],
            "shopname":t[1],
            "username":t[2],
            "itemname":t[3],
            "price":t[4],
            "amount":t[5],
            "date":t[6].strftime("%d/%m/%Y %H:%M:%S")
        }, result
    ))