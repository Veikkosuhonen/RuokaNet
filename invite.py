from app import db
import util
import user_activity
from error import ErrorMessage
from flask import abort

def invite(receivername, shopid):
    """
    Creates a new pending invite whose sender is the session user, receiver is specified by receivername and shop is specified by shopid.
    Adds entries for the sender and the receiver user activity detailing who was invited by whom to which shop.\n
    """
    next = "/shops/" + str(shopid)
    sendername = util.get_username()
    if sendername == None:
        abort(401)
    if not util.owns_shop(shopid):
        abort(403)
    if sendername == receivername:
        raise ErrorMessage("Error: Cannot invite yourself", next=next)
    receiverid = util.get_userid(receivername)
    if receiverid == None:
        raise ErrorMessage(f"User '{receivername}' not found", next=next)
    is_invited = db.session.execute("""
        SELECT invites.id FROM invites WHERE invites.receiverid = :receiverid AND invites.shopid = :shopid AND invites.invitestatus = 0""", 
        {"receiverid":receiverid,"shopid":shopid}).fetchone()
    if is_invited != None:
        raise ErrorMessage(f"User '{receivername}' already has an active invite to this shop", next=next)
    if util.owns_shop(receiverid):
        raise ErrorMessage(f"Error: '{receivername}' is already an owner in this shop", next=next)

    senderid = util.get_userid(sendername)
    db.session.execute(
        "INSERT INTO invites (senderid, receiverid, shopid, invitestatus) VALUES (:senderid, :receiverid, :shopid, 0)",
        {"senderid":senderid, "receiverid":receiverid, "shopid":shopid})

    shopname = db.session.execute("SELECT shopname FROM shops WHERE id = :id", {"id":shopid}).fetchone()[0]
    user_activity.add_activity(senderid, f"You invited {receivername} to {shopname}")
    user_activity.add_activity(receiverid, f"{sendername} invited you to {shopname}")
    db.session.commit()


def update_invite(inviteid, action):
    """
    Updates the invite specified by inviteid with the given action. If action is 'accept',
    adds the user to the owners of the shop, increments the n_owners of the shop and updates the invite status. If the action is 'decline', updates the invite status.
    In both cases new user activity entries are added for the sender and the receiver, detailing the action taken by the receiver. \n
    """

    if not util.is_user():
        abort(403)
    username = util.get_username()
    userid = util.get_userid(username)
    invite = db.session.execute("SELECT id, shopid, senderid FROM invites WHERE receiverid = :userid AND id = :inviteid AND invitestatus = 0", {"userid":userid, "inviteid":inviteid}).fetchone()
    if invite == None:
        abort(404)
    newstatus = 0
    sendername = db.session.execute("SELECT username FROM users WHERE id = :id", {"id":invite[2]}).fetchone()[0]
    shopname = db.session.execute("SELECT shopname FROM shops WHERE id = :id", {"id":invite[1]}).fetchone()[0]
    if action == "accept":
        newstatus = 1
        # become owner
        db.session.execute("INSERT INTO shop_owners (userid, shopid) VALUES (:userid, :shopid)", {"userid":userid,"shopid":invite[1]})
        db.session.execute("UPDATE shops SET n_owners = n_owners + 1 WHERE id = :shopid", {"shopid":invite[1]})
        user_activity.add_activity(userid, f"You accepted {sendername}'s invite to {shopname}")
        user_activity.add_activity(invite[2], f"{username} accepted your invite to {shopname}")
    elif action == "decline":
        newstatus = 2
        user_activity.add_activity(userid, f"You declined {sendername}'s invite to {shopname}")
        user_activity.add_activity(invite[2], f"{username} declined your invite to {shopname}")
    db.session.execute("UPDATE invites SET invitestatus = :status WHERE id = :inviteid", {"inviteid":inviteid, "status":newstatus})
    db.session.commit()