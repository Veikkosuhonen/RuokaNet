from functools import wraps
from flask import session, redirect, url_for, request, flash


def login_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if "username" in session:
            return func(*args, **kwargs)
        else:
            flash("Please login to access this page")
            return redirect(url_for("login", next=request.url))
    return decorated_func


def access_level_required(level=1):
    def decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if "access_level" in session:
                if session["access_level"] >= level:
                    return func(*args, **kwargs)
            flash("Unauthorized")
            if "username" in session:
                return redirect("/")
            else:
                return redirect(url_for("login"))
        return decorated_func
    return decorator