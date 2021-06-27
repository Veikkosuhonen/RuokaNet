from app import db
import util
from transaction import do_buy_transaction
from error import ErrorMessage

def get_products():
    return map(
        lambda p: {
            "itemname": p[0],
            "price": p[1],
            "shopid": p[2],
            "shopname": p[3],
            "quantity": p[4]
        } ,db.session.execute(
        """SELECT items.itemname, products.price, shops.id, shops.shopname, shop_inventory.quantity 
        FROM products, shops, shop_inventory, items 
        WHERE shop_inventory.shopid = shops.id AND shop_inventory.itemid = items.id AND products.shopid = shops.id AND items.id = products.itemid""").fetchall())


def add_product(shopid, itemname, price):
    next = "/shops/" + str(shopid)
    if not util.owns_shop(shopid):
        raise ErrorMessage("Unauthorized: you do not own this shop", next=next)
    itemid = db.session.execute("SELECT id FROM items WHERE itemname = :itemname",{"itemname":itemname}).fetchone()
    if itemid == None:
        raise ErrorMessage(f"Error: item '{itemname}' not found", next=next)
    itemid = itemid[0]
    exists = db.session.execute("SELECT id FROM products WHERE itemid = :itemid AND shopid = :shopid", {"itemid":itemid, "shopid":shopid}).fetchone()
    if exists != None: # shop cannot add same item for sale twice
        raise ErrorMessage(f"Error: {itemname} has already been listed in this shop", next=next)
    productid = db.session.execute(
        "INSERT INTO products (itemid, price, shopid) VALUES (:itemid, :price, :shopid) RETURNING id", 
        {"itemid":itemid, "price":price, "shopid":shopid}).fetchone()[0]
    db.session.execute("INSERT INTO shop_inventory (shopid, itemid, quantity) VALUES (:shopid, :itemid, 0)",{"shopid":shopid, "itemid":itemid})
    db.session.commit()


def change_product_price(productid, price):
    username = util.get_username()
    shopowner = db.session.execute(
        "SELECT shop_owners.shopid FROM users, shop_owners, products WHERE users.username = :username AND users.id = shop_owners.userid AND products.id = :productid AND products.shopid = shop_owners.shopid",
        {"username":username, "productid":productid}).fetchone()
    if shopowner == None:
        raise ErrorMessage("Error: either you do not own the shop or the product does not exist")
    db.session.execute("UPDATE products SET price = :newprice WHERE id = :id", {"id":productid, "newprice":price})
    db.session.commit()


def delete_product(productid, shopid):
    owns_shop_with_product = db.session.execute(
        "SELECT product.id FROM products, shop_owners WHERE product.id = :productid AND product.shopid = :shopid AND shop_owners.userid = :userid AND shop_owners.shopid = :shopid",
        {"productid":productid, "shopid":shopid, "userid":util.get_userid()}).fetchone()
    if owns_shop_with_product == None:
        raise ErrorMessage("Error: either you do not own the shop or the product does not exist")
    db.session.execute("DELETE FROM products WHERE id = :id", {"id":productid})
    db.session.commit()


def buy_product(productid):
    do_buy_transaction(productid, util.get_userid(util.get_username()))


def produce_product(productid, userid):
    product = db.session.execute(
        "SELECT products.itemid, products.shopid FROM products, shop_owners WHERE shop_owners.userid = :userid AND shop_owners.shopid = products.shopid AND products.id = :productid",
        {"productid":productid,"userid":userid}).fetchone()
    if product == None:
        raise ErrorMessage("Error: either you do not own the shop or the product does not exist")
    itemid, shopid = product
    db.session.execute("UPDATE shop_inventory SET quantity = quantity + 1 WHERE shopid = :shopid AND itemid = :itemid",
        {"shopid":shopid,"itemid":itemid})
    db.session.commit()