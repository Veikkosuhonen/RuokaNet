from app import db
import util

def get_shops():
    all_shops = db.session.execute("SELECT id, shopname, active FROM shops").fetchall()
    shop_owners = db.session.execute("SELECT shop_owners.shopid, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid").fetchall()
    # Form a list of unique shops each with a list of owners
    shops = dict()
    for s in all_shops:
        shops[s[0]] = (s[0], s[1], list(), s[2])
    for owner in shop_owners:
        shops[owner[0]][2].append(owner[1])
    return list(shops.values())

def get_shop(id):
    shop = db.session.execute("SELECT id, shopname FROM shops WHERE id = :id", {"id":id}).fetchone()
    if shop == None:
        return 404
    products = db.session.execute(
        """SELECT products.id, items.itemname, products.price, shop_inventory.quantity 
        FROM items, products, shop_inventory 
        WHERE products.shopid = :shopid AND shop_inventory.shopid = :shopid AND shop_inventory.itemid = items.id AND products.itemid = items.id""", 
        {"shopid":id}).fetchall()
    owners = db.session.execute(
        "SELECT users.id, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid AND :shopid = shop_owners.shopid", {"shopid":id}).fetchall()
    return (shop, products, owners)

def get_items():
    return db.session.execute("SELECT id, itemname FROM items").fetchall()

def create_new(username, shopname):
    shop = db.session.execute("SELECT shopname FROM shops WHERE shopname = :name", {"name":shopname}).fetchone()
    print("creating " + shopname)
    if shop != None:
        # Shopname taken
        print("shopname taken")
        return None
    shopid = db.session.execute("INSERT INTO shops (shopname, active) VALUES (:name, 1) RETURNING id", {"name":shopname}).fetchone()[0]
    userid = util.get_userid(username)
    db.session.execute("INSERT INTO shop_owners (userid, shopid) VALUES (:userid, :shopid)", {"userid":userid, "shopid":shopid})
    db.session.commit()
    return shopid

def leave_shop(username, shopid):
    userid = util.get_userid(username)
    db.session.execute("DELETE FROM shop_owners WHERE shop_owners.userid = :userid AND shop_owners.shopid = :shopid", {"userid":userid, "shopid":shopid})
    owners = db.session.execute("SELECT shops.id FROM shops, shop_owners WHERE shops.id = shop_owners.shopid").fetchone()
    if owners == None:
        # shop has no owners left, mark inactive
        db.session.execute("UPDATE shops SET active = 0 WHERE id = :id", {"id":shopid})
    db.session.commit()
    return 200