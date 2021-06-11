from flask import render_template, request, redirect, session, abort

from app import app, db
import util

from transaction import do_transaction, produce_product
from shop import get_shops, get_shop, get_items, create_new, leave_shop
from authentication import do_signup, do_login, do_logout
from user import get_users, get_public_user, get_private_user
from invite import invite, update_invite
from product import get_products, add_product, change_product_price
from stats import get_general_stats

@app.route("/")
def index():
    stats = get_general_stats()
    return render_template("index.html", active='home', stats=stats)

"""
AUTHENTICATION
"""
@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    success = do_signup(username, password)
    if not success:
        redirect("/signup")
    return redirect("/login")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    success = do_login(username, password)
    if not success:
        return redirect("/login")
    return redirect("/")

@app.route("/logout")
def logout():
    do_logout()
    return redirect("/")

"""
USER VIEW
"""
@app.route("/users")
def users():
    return render_template("users.html", users=get_users(), active='users')

@app.route("/users/<string:name>")
def user(name):
    user = None
    if util.user_is(name):
        user = get_private_user(name)
    else: 
        user = get_public_user(name)
    return render_template("user.html", user=user)

"""
SHOP VIEW
"""
@app.route("/shops")
def shops():
    querystring = ""
    if "query" in request.args:
        querystring = request.args["query"]
    filter = None
    if "filter" in request.args:
        filter = request.args["filter"]
    shops = get_shops(querystring, filter)

    return render_template("shops.html", shops=shops, active='shops', filter=filter, querystring=querystring)

@app.route("/shops/<int:id>")
def shop(id):
    result = get_shop(id)
    if result == 404:
        abort(404)
    shop, products, owners = result
    isowner = False
    items = list()
    if util.is_user():
        for owner in owners:
            if owner[1] == session["username"]:
                isowner = True
                items = get_items()
                break
    return render_template("shop.html", shop=shop, products=products, owners=owners, isowner=isowner, items=items)

@app.route("/newshop", methods=["POST"])
def create_new_shop():
    if not util.is_user():
        return render_template("login.html")
    shopid = create_new(session["username"], request.form["shopname"])
    if shopid == None:
        # Shopname taken
        print("shopname taken")
        return redirect("/users/" + session["username"])
    return redirect("/shops/" + str(shopid))

"""
PRODUCT VIEW
"""
@app.route("/products")
def products():
    return render_template("products.html", products=get_products(), active='products')

@app.route("/shops/<int:shopid>/addproduct", methods=["POST"])
def addproduct(shopid):
    code = add_product(shopid, request.form["itemname"], request.form["price"])
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))

@app.route("/shops/<int:shopid>/products/<int:productid>", methods=["POST"])
def changeproductprice(productid, shopid):
    code = change_product_price(productid, request.form["newprice"])
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid)) # shopid


@app.route("/shops/<int:shopid>/products/<int:productid>/delete", methods=["POST"])
def deleteproduct(productid, shopid):
    if not util.is_user():
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
INVITE
"""
@app.route("/shops/<int:shopid>/inviteuser", methods=["POST"])
def inviteuser(shopid):
    code = invite(request.form["receivername"], shopid)
    if code != 200:
        return abort(code)
    return redirect("/shops/" + str(shopid))


@app.route("/invites/<int:inviteid>/<string:action>", methods=["POST"])
def updateinvite(inviteid, action):
    code = update_invite(inviteid, action)
    if code != 200:
        abort(code)
    return redirect("/users/" + session["username"])

"""
LEAVE SHOP
"""
@app.route("/shops/<int:shopid>/leave", methods=["POST"])
def leaveshop(shopid):
    if not util.is_user():
        abort(403)
    code = leave_shop(session["username"], shopid)
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))

"""
PRODUCE PRODUCT
"""
@app.route("/shops/<int:shopid>/produce/<int:productid>", methods=["POST"])
def produce(shopid, productid):
    if not util.is_user():
        return render_template("login.html")
    userid = util.get_userid(session["username"])
    produce_product(productid, userid)
    return redirect("/shops/" + str(shopid))

"""
BUY PRODUCT
"""
@app.route("/shops/<int:shopid>/buy/<int:productid>", methods=["POST"])
def buy(shopid, productid):
    if not util.is_user():
        return render_template("login.html")
    if util.owns_shop(shopid): # cannot buy from self
        abort(403)
    code = do_transaction(productid, util.get_userid(session["username"]))
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))