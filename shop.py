from app import db
import util
import user_activity
from flask import abort
from error import ErrorMessage

def get_shops(querystring, filter):
    """
    Get a list of shop-information in tuples (id, name, list_of_owners, n_owners), filtered by querystring and filter option,
    where the filter should either be 'shop' for shop name, 'owner' for owner name, 'item' for item sold at shop, or empty for no filter.
    """
    sql_like_string = ""
    sql_where_string = " TRUE"
    sql_query_string = "SELECT shops.id, shops.shopname, shops.n_owners, shops.creation_date FROM shops, shop_owners, users, items, products"
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
    #print(sql_query_string)
    all_shops = db.session.execute(sql_query_string, {"querystring": "%"+ querystring +"%"}).fetchall()
    
    shop_owners = db.session.execute("SELECT shop_owners.shopid, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid").fetchall()
    # Form a list of unique shops each with a list of owners
    shops = dict()
    for s in all_shops:
        shops[s[0]] = (s[0], s[1], list(), s[2], s[3])
    for owner in shop_owners:
        if owner[0] in shops.keys():
            shops[owner[0]][2].append(owner[1])
    return map(lambda s: {
        "id":s[0],
        "shopname":s[1],
        "owners": s[2],
        "n_owners": s[3],
        "creation_date": s[4]
    }, shops.values())


def get_shop(id):
    """
    Finds a shop by id (return 404 if not found) and return (shop, products, owners) where shop is (id, name), 
    products is a list [(id, itemname, price, quantity)] and owners is a list [(userid, username)]
    """
    shop = db.session.execute("SELECT id, shopname, n_owners, creation_date FROM shops WHERE id = :id", {"id":id}).fetchone()
    if shop == None:
        abort(404)
    products = db.session.execute(
        """SELECT products.id, items.itemname, products.price, shop_inventory.quantity 
        FROM items, products, shop_inventory 
        WHERE products.shopid = :shopid AND shop_inventory.shopid = :shopid AND shop_inventory.itemid = items.id AND products.itemid = items.id""", 
        {"shopid":id}).fetchall()
    owners = db.session.execute(
        "SELECT users.id, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid AND :shopid = shop_owners.shopid", {"shopid":id}).fetchall()
    return {
        "shopid":shop[0],
        "shopname":shop[1],
        "n_owners":shop[2],
        "creation_date":shop[3],
        "has_products": len(products) > 0,
        "products":products,
        "owners":owners
    }


def create_new(shopname):
    """
    Creates a new shop with the name shopname and owner username. If a shop with the same name exists or the user doesn't exist, aborts and returns None,
    else returns the id of the new shop.
    """
    username = util.get_username()
    next = "/users/" + username
    shop = db.session.execute("SELECT shopname FROM shops WHERE shopname = :name", {"name":shopname}).fetchone()
    print("creating " + shopname)
    if shop != None:
        raise ErrorMessage(f"Shop name '{shopname}' is taken", next=next)
    shopid = db.session.execute("INSERT INTO shops (shopname, n_owners) VALUES (:name, 1) RETURNING id", {"name":shopname}).fetchone()[0]
    userid = util.get_userid(username)
    if userid == None:
        abort(401) # should never happen
    db.session.execute("INSERT INTO shop_owners (userid, shopid) VALUES (:userid, :shopid)", {"userid":userid, "shopid":shopid})
    user_activity.add_activity(userid, f"You created {shopname}")
    db.session.commit()
    return shopid


def leave_shop(username, shopid):
    """
    Removes the owner with the given username from owners of the shop with shopid and decrements the n_owners of the shop.
    """
    userid = util.get_userid(username)
    result = db.session.execute("DELETE FROM shop_owners WHERE userid = :userid AND shopid = :shopid RETURNING shopid", {"userid":userid, "shopid":shopid}).fetchone()
    if result == None:
        # Either no such shop exists or user is not an owner. 
        abort(404)
    db.session.execute("UPDATE shops SET n_owners = n_owners - 1 WHERE id = :shopid", {"shopid": shopid})
    shopname = db.session.execute("SELECT shopname FROM shops WHERE id = :shopid", {"shopid":shopid}).fetchone()[0]
    user_activity.add_activity(userid, f"You left {shopname}")
    db.session.commit()


def get_shops_owned_by(userid):
    all_shops = db.session.execute("""
    SELECT shops.id, shops.shopname, shops.n_owners, shops.creation_date FROM shops, shop_owners 
    WHERE shops.id = shop_owners.shopid AND shop_owners.userid = :userid""", {"userid":userid}).fetchall()
    
    shop_owners = db.session.execute("SELECT shop_owners.shopid, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid").fetchall()
    # Form a list of unique shops each with a list of owners
    shops = dict()
    for s in all_shops:
        shops[s[0]] = (s[0], s[1], list(), s[2], s[3])
    for owner in shop_owners:
        if owner[0] in shops.keys():
            shops[owner[0]][2].append(owner[1])

    return map(lambda s: {
        "id":s[0],
        "shopname":s[1],
        "owners": s[2],
        "n_owners": s[3],
        "creation_date": s[4]
    }, shops.values())