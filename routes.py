from flask import render_template, request, redirect, session, abort, flash

from app import app, db
from error import ErrorMessage
import util
from auth_decorator import login_required, access_level_required, check_csrf

import shop
import authentication
import user
import invite
import product
import stats
import transaction
import item


@app.route("/")
def index():
    stat = stats.get_general_stats()
    return render_template("index.html", active='home', stats=stat)


"""
AUTHENTICATION
""" 
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", usernames=list(map(lambda x: x[1], users.get_users())))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success = authentication.do_signup(username, password)
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
        authentication.do_login(username, password)
        return redirect("/")


@app.route("/logout")
@login_required
def logout():
    authentication.do_logout()
    return redirect("/")


"""
USER VIEW
"""
@app.route("/users")
def users():
    return render_template("users.html", users=user.get_users(), active='users')


@app.route("/users/<string:name>")
def user_view(name):
    if util.user_is(name):
        user_data = user.get_private_user(name)
        return render_template("private_user.html", user=user_data)
    else: 
        user_data = user.get_public_user(name)
        return render_template("public_user.html", user=user_data)


"""
ITEMS
"""
@app.route("/items")
def items():
    items = item.get_items()
    return render_template("items.html", items=items, active='items')


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
    shops = shop.get_shops(querystring, filter)

    return render_template("shops.html", shops=shops, active='shops', filter=filter, querystring=querystring)


@app.route("/shops/<int:id>")
def shop_view(id):
    shop_data = shop.get_shop(id)

    # check if is owner and add the list of items to template
    isowner = False
    items = list()
    if util.is_user():
        for owner in shop_data["owners"]:
            if owner[1] == session["username"]:
                isowner = True
                items = item.get_items_id_name()
                break
    return render_template("shop.html", shop=shop_data, isowner=isowner, items=items)


@app.route("/newshop", methods=["POST"])
@login_required
@check_csrf
def create_new_shop():
    shopid = shop.create_new(session["username"], request.form["shopname"])
    return redirect("/shops/" + str(shopid))


"""
PRODUCT VIEW
"""
@app.route("/products")
def products():
    return render_template("products.html", products=product.get_products(), active='products')


@app.route("/shops/<int:shopid>/addproduct", methods=["POST"])
@login_required
@check_csrf
def addproduct(shopid):
    product.add_product(shopid, request.form["itemname"], request.form["price"])
    return redirect("/shops/" + str(shopid))


@app.route("/shops/<int:shopid>/products/<int:productid>", methods=["POST"])
@login_required
@check_csrf
def changeproductprice(productid, shopid):
    product.change_product_price(productid, request.form["newprice"])
    return redirect("/shops/" + str(shopid)) # shopid


@app.route("/shops/<int:shopid>/products/<int:productid>/delete", methods=["POST"])
@login_required
@check_csrf
def deleteproduct(productid, shopid):
    product.delete_product(productid, shopid)
    return redirect("/shops/" + str(shopid))


"""
INVITE
"""
@app.route("/shops/<int:shopid>/inviteuser", methods=["POST"])
@login_required
@check_csrf
def inviteuser(shopid):
    username = request.form["receivername"]
    invite.invite(username, shopid)
    return redirect("/shops/" + str(shopid))


@app.route("/invites/<int:inviteid>/<string:action>", methods=["POST"])
@login_required
@check_csrf
def updateinvite(inviteid, action):
    invite.update_invite(inviteid, action)
    return redirect("/users/" + session["username"])


"""
LEAVE SHOP
"""
@app.route("/shops/<int:shopid>/leave", methods=["POST"])
@login_required
@check_csrf
def leaveshop(shopid):
    shop.leave_shop(session["username"], shopid)
    return redirect("/shops/" + str(shopid))


"""
PRODUCE PRODUCT
"""
@app.route("/shops/<int:shopid>/produce/<int:productid>", methods=["POST"])
@login_required
@check_csrf
def produce(shopid, productid):
    userid = util.get_userid(session["username"])
    product.produce_product(productid, userid)
    return redirect("/shops/" + str(shopid))


"""
BUY PRODUCT
"""
@app.route("/shops/<int:shopid>/buy/<int:productid>", methods=["POST"])
@login_required
@check_csrf
def buy(shopid, productid):
    product.buy_product(productid)
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
    transactions = transaction.get_transactions(querystring, filter)

    return render_template("transactions.html", transactions=transactions, active='transactions', filter=filter, querystring=querystring)