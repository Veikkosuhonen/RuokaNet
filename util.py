from flask import session
from app import db


def is_user():
    return "username" in session


def user_is(username):
    if is_user():
        return session["username"] == username
    return False


def owns_shop(userid, shopid):
    owner = db.session.execute(
        "SELECT shop_owners.userid FROM shop_owners WHERE :userid= shop_owners.userid AND :shopid = shop_owners.shopid", 
        {"userid":userid,"shopid":shopid}).fetchone()
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