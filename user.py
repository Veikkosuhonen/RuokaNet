from app import db
import util

def get_users():

    return db.session.execute("SELECT id, username, (SELECT COUNT(userid) FROM shop_owners WHERE userid = users.id) FROM users").fetchall()

def get_public_user(name):
    userid = util.get_userid(name)
    if userid == None:
        return None
    shops = db.session.execute(
        "SELECT shops.id, shops.shopname FROM shops, shop_owners WHERE :userid = shop_owners.userid AND shops.id = shop_owners.shopid", {"userid":userid}).fetchall()    
    return ((userid, name), shops)

def get_private_user(name):
    userid = util.get_userid(name)
    if userid == None:
        return None
    shops = db.session.execute(
        "SELECT shops.id, shops.shopname FROM shops, shop_owners WHERE :userid = shop_owners.userid AND shops.id = shop_owners.shopid", {"userid":userid}).fetchall()
    balance = db.session.execute("SELECT balance FROM users WHERE id = :userid",{"userid":userid}).fetchone()[0]
    inventory = db.session.execute("""
        SELECT items.itemname, user_inventory.quantity FROM items, user_inventory
        WHERE user_inventory.userid = :userid AND user_inventory.itemid = items.id AND user_inventory.quantity > 0""",
        {"userid":userid}).fetchall()
    # Get the private profile activity stuff
    incoming_invites = db.session.execute(
        "SELECT invites.id, users.username, shops.shopname, invites.invitestatus FROM users, shops, invites WHERE users.id = invites.senderid AND shops.id = invites.shopid AND invites.receiverid = :userid",
        {"userid":userid}).fetchall()
    sent_invites = db.session.execute(
        "SELECT invites.id, users.username, shops.shopname, invites.invitestatus FROM users, shops, invites WHERE users.id = invites.receiverid AND shops.id = invites.shopid AND invites.senderid = :userid",
        {"userid":userid}).fetchall()
    pending_incoming_invites = [invite for invite in incoming_invites if invite[3] == 0]
    pending_sent_invites = [invite for invite in sent_invites if invite[3] == 0]
    activity = [] # TODO activity (description, timestamp)
    return ((userid, name), shops, pending_incoming_invites, pending_sent_invites, balance, inventory)