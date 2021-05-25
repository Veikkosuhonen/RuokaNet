from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

def do_signup(username, password):
    user = db.session.execute("SELECT username FROM users WHERE username = :name", {"name":username}).fetchone()
    print("signing up as " + username)
    if user != None:
        # Username taken
        print("username taken")
        return False
    pwhash = generate_password_hash(password)
    db.session.execute("INSERT INTO users (username, password, balance) VALUES (:name, :pwhash, 1000.0)", {"name":username, "pwhash":pwhash})
    db.session.commit()
    print("success")
    return True


def do_login(username, password):
    print("loggin in as " + username)

    user = db.session.execute("SELECT password FROM users WHERE username = :username", {"username":username}).fetchone()
    if user == None:
        print("username does not exist")
        return False
    else:
        pwhash = user[0]
        if check_password_hash(pwhash, password):
            session["username"] = username
            print("success")
            return True
        else:
            print("wrong password")
            return False

def do_logout():
    del session["username"]