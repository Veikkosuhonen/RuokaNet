from app import db


def get_general_stats():
    n_shops = db.session.execute("SELECT COUNT(id) FROM shops").fetchone()[0]
    n_owners = db.session.execute("SELECT COUNT(DISTINCT userid) FROM shop_owners").fetchone()[0]
    n_items_for_sale = db.session.execute("SELECT COUNT(DISTINCT itemid) FROM products").fetchone()[0]
    n_units_for_sale = db.session.execute("SELECT SUM(quantity) FROM shop_inventory").fetchone()[0]
    return (n_shops, n_owners, n_items_for_sale, n_units_for_sale)