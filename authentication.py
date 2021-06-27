from flask import session
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import user_activity
from error import ErrorMessage

def do_signup(username, password):
    if len(username) < 1 or len(username) > 16 or len(password) < 1 or len(password) > 16:
        raise ErrorMessage("Invalid username or password. Username and password must be between 1 and 16 characters")
    user = db.session.execute("SELECT username FROM users WHERE username = :name", {"name":username}).fetchone()
    if user != None:
        # Username taken
        raise ErrorMessage(f"Username '{username}' is taken", next="/signup")
    pwhash = generate_password_hash(password)
    userid = db.session.execute("INSERT INTO users (username, password, balance) VALUES (:name, :pwhash, 1000.0) RETURNING id", {"name":username, "pwhash":pwhash}).fetchone()[0]
    user_activity.add_activity(userid, f"{username} joined VirtualMarket")
    db.session.commit()


def do_login(username, password):

    user = db.session.execute("SELECT password, access_level FROM users WHERE username = :username", {"username":username}).fetchone()
    if user == None:
        raise ErrorMessage("Invalid username", next="/login")
    else:
        pwhash = user[0]
        if check_password_hash(pwhash, password):
            session["username"] = username
            session["access_level"] = user[1]
            session["csrf_token"] = secrets.token_hex(16)
        else:
            raise ErrorMessage("Wrong password", next="/login")


def do_logout():
    del session["username"]
    del session["access_level"]
    del session["csrf_token"]
