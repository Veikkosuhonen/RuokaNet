from flask import session
from app import db


def is_user():
    return "username" in session


def user_is(username):
    if is_user():
        return session["username"] == username
    return False


def owns_shop(id):
    if not is_user():
        return False
    owner = db.session.execute(
        "SELECT users.username FROM users, shop_owners WHERE users.id = shop_owners.userid AND :shopid = shop_owners.shopid AND users.username = :username", 
        {"shopid":id, "username":session["username"]}).fetchone()
    return owner != None


def get_userid(name):
    result = db.session.execute("SELECT id FROM users WHERE username = :name", {"name": name}).fetchone()
    if result == None:
        return None
    return result[0]


def get_username():
    if is_user():
        return session["username"]
    else:
        return None