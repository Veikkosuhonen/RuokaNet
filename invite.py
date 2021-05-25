from app import db
import util

def invite(receivername, shopid):
    sendername = util.get_username()
    if sendername == None:
        return 403
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
    db.session.commit()
    return 200


def update_invite(inviteid, action):
    if not util.is_user():
        return 403
    userid = util.get_userid(session["username"])
    invite = db.session.execute("SELECT id, shopid FROM invites WHERE receiverid = :userid AND id = :inviteid AND invitestatus = 0", {"userid":userid, "inviteid":inviteid}).fetchone()
    if invite == None:
        return 404
    newstatus = 0
    if action == "accept":
        newstatus = 1
        # become owner
        db.session.execute("INSERT INTO shop_owners (userid, shopid) VALUES (:userid, :shopid)", {"userid":userid,"shopid":invite[1]})
    elif action == "decline":
        newstatus = 2
    db.session.execute("UPDATE invites SET invitestatus = :status WHERE id = :inviteid", {"inviteid":inviteid, "status":newstatus})
    db.session.commit()
    return 200


