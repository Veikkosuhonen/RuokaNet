from flask import render_template, request, redirect, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db


"""
HELPERS
"""
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

def owns_product(id):
    if not is_user():
        return False
    username = session["username"]
    shopowner = db.session.execute(
        "SELECT shop_owners.shopid FROM users, shop_owners, products WHERE users.username = :username AND users.id = shop_owners.userid AND products.id = :productid AND products.shopid = shop_owners.shopid",
        {"username":username, "productid":id}).fetchone()
    return shopowner != None

def get_userid(name):
    result = db.session.execute("SELECT id FROM users WHERE username = :name", {"name": name}).fetchone()
    if result == None:
        return None
    return result[0]

"""
ROUTING
"""

@app.route("/")
def index():
    return render_template("index.html")

"""
AUTHENTICATION
"""
@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    user = db.session.execute("SELECT username FROM users WHERE username = :name", {"name":username}).fetchone()
    print("signing up as " + username)
    if user != None:
        # Username taken
        print("username taken")
        return redirect("/login")
    password = request.form["password"]
    pwhash = generate_password_hash(password)
    db.session.execute("INSERT INTO users (username, password) VALUES (:name, :pwhash)", {"name":username, "pwhash":pwhash})
    db.session.commit()
    print("success")
    return redirect("/login")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print("loggin in as " + username)

    user = db.session.execute("SELECT password FROM users WHERE username = :username", {"username":username}).fetchone()
    if user == None:
        print("username does not exist")
        return redirect("/login")
    else:
        pwhash = user[0]
        if check_password_hash(pwhash, password):
            session["username"] = username
            print("success")
            return redirect("/")
        else:
            print("wrong password")
            return redirect("/login")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

"""
USER VIEW
"""
@app.route("/users")
def users():
    sql = "SELECT id, username FROM users"
    result = db.session.execute(sql)
    users = result.fetchall()
    return render_template("users.html", users=users)

@app.route("/users/<string:name>")
def user(name):
    userid = get_userid(name)
    if userid == None:
        abort(404)
    shops = db.session.execute(
        "SELECT shops.id, shops.shopname FROM shops, shop_owners WHERE :userid = shop_owners.userid AND shops.id = shop_owners.shopid", {"userid":userid}).fetchall()
    if user_is(name):
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
        return render_template("user.html", user=(userid, name), shops=shops, incoming_invites=pending_incoming_invites, sent_invites=pending_sent_invites)
    return render_template("user.html", user=(userid, name), shops=shops)

"""
SHOP VIEW
"""
@app.route("/shops")
def shops():
    all_shops = db.session.execute("SELECT id, shopname, active FROM shops").fetchall()
    shop_owners = db.session.execute("SELECT shop_owners.shopid, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid").fetchall()
    # Form a list of unique shops each with a list of owners
    shops = dict()
    for s in all_shops:
        shops[s[0]] = (s[0], s[1], list(), s[2])
    for owner in shop_owners:
        shops[owner[0]][2].append(owner[1])
    return render_template("shops.html", shops=list(shops.values()))

@app.route("/shops/<int:id>")
def shop(id):
    result = db.session.execute("SELECT id, shopname FROM shops WHERE id = :id", {"id":id}).fetchone()
    products = db.session.execute(
        "SELECT products.id, products.productname, products.price FROM products WHERE products.shopid = :shopid", {"shopid":id}).fetchall()
    owners = db.session.execute(
        "SELECT users.id, users.username FROM users, shop_owners WHERE users.id = shop_owners.userid AND :shopid = shop_owners.shopid", {"shopid":id}).fetchall()
    return render_template("shop.html", shop=result, products=products, owners=owners, isowner=owns_shop(id))

@app.route("/newshop", methods=["POST"])
def create_new_shop():
    if not is_user():
        return render_template("login.html")
    shopname = request.form["shopname"]
    ownername = session["username"]
    shop = db.session.execute("SELECT shopname FROM shops WHERE shopname = :name", {"name":shopname}).fetchone()
    print("creating " + shopname)
    if shop != None:
        # Shopname taken
        print("shopname taken")
        return redirect("/users/" + session["username"])
    db.session.execute("INSERT INTO shops (shopname, active) VALUES (:name, 1)", {"name":shopname})
    shopid = db.session.execute("SELECT id FROM shops WHERE shopname = :name", {"name":shopname}).fetchone()[0]
    userid = db.session.execute("SELECT id FROM users WHERE username = :name", {"name":ownername}).fetchone()[0]
    db.session.execute("INSERT INTO shop_owners (userid, shopid) VALUES (:userid, :shopid)", {"userid":userid, "shopid":shopid})
    db.session.commit()
    return redirect("/users/" + session["username"])

"""
PRODUCT VIEW
"""
@app.route("/products")
def products():
    products = db.session.execute("SELECT products.productname, products.price, shops.id, shops.shopname FROM products, shops WHERE products.shopid = shops.id")
    return render_template("products.html", products=products)

@app.route("/shops/<int:id>/addproduct", methods=["POST"])
def add_product(id):
    if not is_user():
        return render_template("login.html")
    if not owns_shop(id):
        abort(403)
    productname = request.form["name"]
    price = request.form["price"]
    db.session.execute("INSERT INTO products (productname, price, shopid) VALUES (:name, :price, :id)", {"name":productname, "price":price, "id":id})
    db.session.commit()
    return redirect("/shops/" + str(id))

@app.route("/products/<int:id>", methods=["POST"])
def change_product_price(id):
    if not is_user():
        return render_template("login.html")
    username = session["username"]
    shopowner = db.session.execute(
        "SELECT shop_owners.shopid FROM users, shop_owners, products WHERE users.username = :username AND users.id = shop_owners.userid AND products.id = :productid AND products.shopid = shop_owners.shopid",
        {"username":username, "productid":id}).fetchone()
    if shopowner == None:
        # Does not own the shop
        abort(403)
    newprice = request.form["newprice"]
    db.session.execute("UPDATE products SET price = :newprice WHERE id = :id", {"id":id, "newprice":newprice})
    db.session.commit()
    return redirect("/shops/" + str(shopowner[0])) # shopid

"""
@app.route("/products/<int:id>/delete", methods=["POST"])
def delete_product(id):
    if not is_user():
        return render_template("login.html")
    username = session["username"]
    shopowner = db.session.execute(
        "SELECT shop_owners.shopid FROM users, shop_owners, products WHERE users.username = :username AND users.id = shop_owners.userid AND products.id = :productid AND products.shopid = shop_owners.shopid",
        {"username":username, "productid":id}).fetchone()
    if shopowner == None:
        # Does not own the shop
        abort(403)
    db.session.execute("DELETE FROM products WHERE id = :id", {"id":id})
    db.session.commit()
    return redirect("/shops/" + str(shopowner[0])) # shopid
"""

"""
INVITE
"""
@app.route("/shops/<int:shopid>/inviteuser", methods=["POST"])
def invite(shopid):
    if not is_user():
        return render_template("login.html")
    if not owns_shop(shopid):
        print("doesnt own shop")
        abort(403)
    receivername = request.form["receivername"]
    if receivername == session["username"]:
        print("cannot invite self")
        abort(403)
    print("inviting " + receivername + " for shop " + str(shopid))
    receiver = db.session.execute( # get the receiver who is not an owner nor has an invite to the shop
        """SELECT U.id, U.username 
        FROM users U, shop_owners S 
        WHERE U.username = :username 
        // receiver not an owner of the shop
        AND U.id = S.userid AND NOT S.shopid = :shopid 
        // receiver does not have an active invite to the shop
        AND U.id NOT IN (SELECT users.id FROM users, invites WHERE users.id = invites.receiverid AND invites.shopid = :shopid AND invites.invitestatus = 0)""",
        {"username":receivername, "shopid":shopid}).fetchone()
    if receiver == None:
        # TODO handle receiver already owner, receiver already invited, receiver does not exist
        abort(404)
    senderid = db.session.execute("SELECT id FROM users WHERE username = :username", {"username":session["username"]}).fetchone()[0]
    db.session.execute(
        "INSERT INTO invites (senderid, receiverid, shopid, invitestatus) VALUES (:senderid, :receiverid, :shopid, 0)",
        {"senderid":senderid, "receiverid":receiver[0], "shopid":shopid})
    db.session.commit()
    return redirect("/shops/" + str(shopid))


@app.route("/invites/<int:inviteid>/<string:action>", methods=["POST"])
def updateinvite(inviteid, action):
    if not is_user():
        return render_template("login.html")
    userid = get_userid(session["username"])
    invite = db.session.execute("SELECT id, shopid FROM invites WHERE receiverid = :userid AND id = :inviteid AND invitestatus = 0", {"userid":userid, "inviteid":inviteid}).fetchone()
    if invite == None:
        abort(404)
    if inviteid == invite[0]:
        newstatus = 0
        if action == "accept":
            newstatus = 1
            # become owner
            db.session.execute("INSERT INTO shop_owners (userid, shopid) VALUES (:userid, :shopid)", {"userid":userid,"shopid":invite[1]})
        elif action == "decline":
            newstatus = 2
        db.session.execute("UPDATE invites SET invitestatus = :status WHERE id = :inviteid", {"inviteid":inviteid, "status":newstatus})
        db.session.commit()
    return redirect("/users/" + session["username"])

"""
LEAVE SHOP
"""
@app.route("/shops/<int:id>/leave", methods=["POST"])
def leaveshop(id):
    if not owns_shop(id):
        abort(403)
    userid = get_userid(session["username"])
    db.session.execute("DELETE FROM shop_owners WHERE shop_owners.userid = :userid AND shop_owners.shopid = :shopid", {"userid":userid, "shopid":id})
    owners = db.session.execute("SELECT shops.id FROM shops, shop_owners WHERE shops.id = shop_owners.shopid").fetchone()
    if owners == None:
        # shop has no owners left, mark inactive
        db.session.execute("UPDATE shops SET active = 0 WHERE id = :id", {"id":id})
    db.session.commit()
    return redirect("/shops/" + str(id))
