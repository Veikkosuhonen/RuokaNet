from flask import render_template, request, redirect, session, abort, flash

from app import app, db
from error import ErrorMessage
import util
from auth_decorator import login_required, access_level_required, check_csrf

from shop import get_shops, get_shop, get_items, create_new, leave_shop
from authentication import do_signup, do_login, do_logout
from user import get_users, get_public_user, get_private_user
from invite import invite, update_invite
from product import get_products, add_product, change_product_price, delete_product, buy_product, produce_product
from stats import get_general_stats
from transaction import get_transactions

@app.route("/")
def index():
    stats = get_general_stats()
    return render_template("index.html", active='home', stats=stats)


"""
AUTHENTICATION
""" 
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", usernames=list(map(lambda x: x[1], get_users())))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = do_signup(username, password)
        if not success:
            raise ErrorMessage("Registration failed, invalid credentials", next="/signup")
        return redirect("/login")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = do_login(username, password)
        if not success:
            raise ErrorMessage("Invalid username or password", next="/login")
        return redirect("/")


@app.route("/logout")
@login_required
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
        return render_template("private_user.html", user=user)
    else: 
        user = get_public_user(name)
        return render_template("public_user.html", user=user)
    

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
    shop = get_shop(id)
    if shop == 404:
        abort(404)

    # check if is owner and add the list of items to template
    isowner = False
    items = list()
    if util.is_user():
        for owner in shop["owners"]:
            if owner[1] == session["username"]:
                isowner = True
                items = get_items()
                break
    return render_template("shop.html", shop=shop, isowner=isowner, items=items)


@app.route("/newshop", methods=["POST"])
@login_required
@check_csrf
def create_new_shop():
    shopid = create_new(session["username"], request.form["shopname"])
    if shopid == None:
        # Shopname taken
        raise ErrorMessage(f"Error: shop name {request.form['shopname']} is taken", next="/users/" + session["username"])
    return redirect("/shops/" + str(shopid))


"""
PRODUCT VIEW
"""
@app.route("/products")
def products():
    return render_template("products.html", products=get_products(), active='products')


@app.route("/shops/<int:shopid>/addproduct", methods=["POST"])
@login_required
@check_csrf
def addproduct(shopid):
    code = add_product(shopid, request.form["itemname"], request.form["price"])
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))


@app.route("/shops/<int:shopid>/products/<int:productid>", methods=["POST"])
@login_required
@check_csrf
def changeproductprice(productid, shopid):
    code = change_product_price(productid, request.form["newprice"])
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid)) # shopid


@app.route("/shops/<int:shopid>/products/<int:productid>/delete", methods=["POST"])
@login_required
@check_csrf
def deleteproduct(productid, shopid):
    code = delete_product(productid, shopid)
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))


"""
INVITE
"""
@app.route("/shops/<int:shopid>/inviteuser", methods=["POST"])
@login_required
@check_csrf
def inviteuser(shopid):
    username = request.form["receivername"]
    code = invite(username, shopid)
    if code != 200:
        if code == 404:
            raise ErrorMessage(f"User '{username}' not found", next="/shops/" + str(shopid))
        elif code == 406:
            raise ErrorMessage(f"User '{username}' already has an active invite to this shop", next="/shops/" + str(shopid))
        abort(code)
    return redirect("/shops/" + str(shopid))


@app.route("/invites/<int:inviteid>/<string:action>", methods=["POST"])
@login_required
@check_csrf
def updateinvite(inviteid, action):
    code = update_invite(inviteid, action)
    if code != 200:
        abort(code)
    return redirect("/users/" + session["username"])


"""
LEAVE SHOP
"""
@app.route("/shops/<int:shopid>/leave", methods=["POST"])
@login_required
@check_csrf
def leaveshop(shopid):
    code = leave_shop(session["username"], shopid)
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))


"""
PRODUCE PRODUCT
"""
@app.route("/shops/<int:shopid>/produce/<int:productid>", methods=["POST"])
@login_required
@check_csrf
def produce(shopid, productid):
    userid = util.get_userid(session["username"])
    produce_product(productid, userid)
    return redirect("/shops/" + str(shopid))


"""
BUY PRODUCT
"""
@app.route("/shops/<int:shopid>/buy/<int:productid>", methods=["POST"])
@login_required
@check_csrf
def buy(shopid, productid):
    code = buy_product(productid)
    if code != 200:
        abort(code)
    return redirect("/shops/" + str(shopid))


"""
TRANSACTIONS
"""
@app.route("/transactions", methods=["GET"])
@access_level_required(level=1)
def transactions():
    querystring = ""
    if "query" in request.args:
        querystring = request.args["query"]
    filter = None
    if "filter" in request.args:
        filter = request.args["filter"]
    transactions = get_transactions(querystring, filter)

    return render_template("transactions.html", transactions=transactions, active='transactions', filter=filter, querystring=querystring)