from app import db
import util

def get_products():
    return db.session.execute(
        """SELECT items.itemname, products.price, shops.id, shops.shopname, shop_inventory.quantity 
        FROM products, shops, shop_inventory, items 
        WHERE shop_inventory.shopid = shops.id AND products.shopid = shops.id AND items.id = products.itemid""").fetchall()

def add_product(shopid, itemid, price):
    if not util.owns_shop(shopid):
        return 403
    item = db.session.execute("SELECT id FROM items WHERE id = :itemid",{"itemid":itemid}).fetchone()
    if item == None:
        return 404
    productid = db.session.execute(
        "INSERT INTO products (itemid, price, shopid) VALUES (:itemid, :price, :shopid) RETURNING id", 
        {"itemid":itemid, "price":price, "shopid":shopid}).fetchone()[0]
    db.session.execute("INSERT INTO shop_inventory (shopid, itemid, quantity) VALUES (:shopid, :itemid, 0)",{"shopid":shopid, "itemid":itemid})
    db.session.commit()
    return 200

def change_product_price(productid, price):
    if not util.is_user():
        return 403
    username = util.get_username()
    shopowner = db.session.execute(
        "SELECT shop_owners.shopid FROM users, shop_owners, products WHERE users.username = :username AND users.id = shop_owners.userid AND products.id = :productid AND products.shopid = shop_owners.shopid",
        {"username":username, "productid":product}).fetchone()
    if shopowner == None:
        # Does not own the shop
        return 403
    db.session.execute("UPDATE products SET price = :newprice WHERE id = :id", {"id":productid, "newprice":price})
    db.session.commit()
    return redirect("/shops/" + str(shopowner[0])) # shopid