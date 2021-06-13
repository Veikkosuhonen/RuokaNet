from app import db
import util
import user_activity


def invite(receivername, shopid):
    """
    Creates a new pending invite whose sender is the session user, receiver is specified by receivername and shop is specified by shopid.
    Adds entries for the sender and the receiver user activity detailing who was invited by whom to which shop.\n
    Returns \n
    - 403 if not logged in or receivername equals session username \n
    - 404 if the receiver cannot be found, the shop cannot be found, the sender is not an owner of the shop, the receiver already is an owner or the receiver already
    has a pending invite to the shop from the sender\n
    - 200 if the operation succeeds \n
    """
    sendername = util.get_username()
    if sendername == None:
        return 401
    if not util.owns_shop(shopid):
        print("doesnt own shop")
        return 403
    if sendername == receivername:
        print("cannot invite self")
        return 403
    print("inviting " + receivername + " for shop " + str(shopid))
    receiver = db.session.execute( # get the receiver who is not an owner nor has an invite to the shop
        """SELECT U.id 
        FROM users U, shop_owners S 
        WHERE U.username = :username 
        /* receiver not an owner of the shop */
        AND U.id = S.userid AND NOT S.shopid = :shopid 
        /* receiver does not have an active invite to the shop */
        AND U.id NOT IN (SELECT users.id FROM users, invites WHERE users.id = invites.receiverid AND invites.shopid = :shopid AND invites.invitestatus = 0)""",
        {"username":receivername, "shopid":shopid}).fetchone()
    if receiver == None:
        # TODO handle receiver already owner, receiver already invited, receiver does not exist
        return 404
    receiverid = receiver[0]
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


