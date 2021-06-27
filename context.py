from app import app
from flask import session

@app.context_processor
def inject_csrf_token():
    if "csrf_token" in session:
        return dict(csrf_token=session["csrf_token"])
    else:
        return dict()