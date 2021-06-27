from app import db
import util
import user_activity


def invite(receivername, shopid):
    """
    Creates a new pending invite whose sender is the session user, receiver is specified by receivername and shop is specified by shopid.
    Adds entries for the sender and the receiver user activity detailing who was invited by whom to which shop.\n
    Returns \n
    - 401 if not logged in \n
    - 403 if receivername equals session username, user doesnt own the shop or receiver owns the shop \n
    - 404 if the receiver cannot be found\n
    - 406 if the receiver has already has an active invite\n
    - 200 if the operation succeeds
    """
    sendername = util.get_username()
    if sendername == None:
        return 401 # should never happen
    if not util.owns_shop(shopid):
        print("doesnt own shop")
        return 403 # can happen if browser validation fails
    if sendername == receivername:
        print("cannot invite self")
        return 403 # can happen if browser validation fails
    receiverid = util.get_userid(receivername)
    if receiverid == None:
        return 404 # happens commonly
    is_invited = db.session.execute("""
        SELECT invites.id FROM invites WHERE invites.receiverid = :receiverid AND invites.shopid = :shopid AND invites.invitestatus = 0""", 
        {"receiverid":receiverid,"shopid":shopid}).fetchone()
    if is_invited != None:
        return 406 # happens commonly
    if util.owns_shop(receiverid):
        return 403 # can happen if browser validation fails

    senderid = util.get_userid(sendername)
    db.session.execute(
        "INSERT INTO invites (senderid, receiverid, shopid, invitestatus) VALUES (:senderid, :receiverid, :shopid, 0)",
        {"senderid":senderid, "receiverid":receiverid, "shopid":shopid})

    shopname = db.session.execute("SELECT shopname FROM shops WHERE id = :id", {"id":shopid}).fetchone()[0]
    user_activity.add_activity(senderid, f"You invited {receivername} to {shopname}")
    user_activity.add_activity(receiverid, f"{sendername} invited you to {shopname}")
    db.session.commit()
    return 200


def update_invite(inviteid, action):
    """
    Updates the invite specified by inviteid with the given action. If action is 'accept',
    adds the user to the owners of the shop, increments the n_owners of the shop and updates the invite status. If the action is 'decline', updates the invite status.
    In both cases new user activity entries are added for the sender and the receiver, detailing the action taken by the receiver. \n
    Returns \n
    - 403 if not logged in \n
    - 404 if there is no invite with inviteid and userid of the session user \n
    - 200 if the operation succeeds \n
    """
    if not util.is_user():
        return 403
    username = util.get_username()
    userid = util.get_userid(username)
    invite = db.session.execute("SELECT id, shopid, senderid FROM invites WHERE receiverid = :userid AND id = :inviteid AND invitestatus = 0", {"userid":userid, "inviteid":inviteid}).fetchone()
    if invite == None:
        return 404
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
    return 200


