from app import db
import util


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
    if not util.owns_shop(shopid):
        return 403
    itemid = db.session.execute("SELECT id FROM items WHERE itemname = :itemname",{"itemname":itemname}).fetchone()
    if itemid == None:
        return 404
    itemid = itemid[0]
    exists = db.session.execute("SELECT id FROM products WHERE itemid = :itemid AND shopid = :shopid", {"itemid":itemid, "shopid":shopid}).fetchone()
    if exists != None: # shop cannot add same item for sale twice
        return 403
    productid = db.session.execute(
        "INSERT INTO products (itemid, price, shopid) VALUES (:itemid, :price, :shopid) RETURNING id", 
        {"itemid":itemid, "price":price, "shopid":shopid}).fetchone()[0]
    db.session.execute("INSERT INTO shop_inventory (shopid, itemid, quantity) VALUES (:shopid, :itemid, 0)",{"shopid":shopid, "itemid":itemid})
    db.session.commit()
    return 200


def change_product_price(productid, price):
    username = util.get_username()
    shopowner = db.session.execute(
        "SELECT shop_owners.shopid FROM users, shop_owners, products WHERE users.username = :username AND users.id = shop_owners.userid AND products.id = :productid AND products.shopid = shop_owners.shopid",
        {"username":username, "productid":productid}).fetchone()
    if shopowner == None:
        # Does not own the shop
        return 403
    db.session.execute("UPDATE products SET price = :newprice WHERE id = :id", {"id":productid, "newprice":price})
    db.session.commit()
    return 200 # shopid


def delete_product(productid, shopid):
    owns_shop_with_product = db.session.execute(
        "SELECT product.id FROM products, shop_owners WHERE product.id = :productid AND product.shopid = :shopid AND shop_owners.userid = :userid AND shop_owners.shopid = :shopid",
        {"productid":productid, "shopid":shopid, "userid":util.get_userid()}).fetchone()
    if owns_shop_with_product == None:
        return 403
    db.session.execute("DELETE FROM products WHERE id = :id", {"id":productid})
    db.session.commit()
    return 200