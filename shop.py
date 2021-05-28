from app import db
import util

def get_shops(querystring, filter):
    sql_like_string = ""
    sql_where_string = " TRUE"
    sql_query_string = "SELECT shops.id, shops.shopname, shops.active FROM shops, shop_owners, users, items, products"
    if querystring != "":
        if filter == "shop":
            sql_like_string += " OR LOWER(shops.shopname) LIKE LOWER(:querystring)"
        elif filter == "owner":
            sql_like_string += " OR LOWER(users.username) LIKE LOWER(:querystring)"
            sql_where_string += " AND shops.id = shop_owners.shopid AND shop_owners.userid = users.id"
        elif filter == "item":
            sql_like_string += " OR LOWER(items.itemname) LIKE LOWER(:querystring)"
            sql_where_string += " AND products.shopid = shops.id AND products.itemid = items.id"
        if sql_like_string != "":
            sql_query_string += " WHERE" + sql_where_string + " AND (FALSE" + sql_like_string + ")"
    print(sql_query_string)
    all_shops = db.session.execute(sql_query_string, {"querystring": "%"+ querystring +"%"}).fetchall()
    
    shop_owners = db.session.execute("SELECT shop_owners.shopid, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid").fetchall()
    # Form a list of unique shops each with a list of owners
    shops = dict()
    for s in all_shops:
        shops[s[0]] = (s[0], s[1], list(), s[2])
    for owner in shop_owners:
        if owner[0] in shops.keys():
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