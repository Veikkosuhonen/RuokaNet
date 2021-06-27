from app import db

def get_items():
    items = db.session.execute("""
        SELECT items.itemname,
        MIN(products.price),
        SUM(shop_inventory.quantity) 
        FROM items, products, shop_inventory
        WHERE items.id = products.itemid AND items.id = shop_inventory.itemid AND products.shopid = shop_inventory.shopid AND shop_inventory.quantity > 0 
        GROUP BY items.itemname""").fetchall()
    return list(map(lambda i:{
        "itemname":i[0],
        "min_price":i[1],
        "total_units":i[2]
    }, items))


def get_items_id_name():
    """
    Returns [(id, itemname)]
    """
    return db.session.execute("SELECT id, itemname FROM items").fetchall()