from app import app
from flask import request, redirect, flash

class ErrorMessage(Exception):
    def __init__(self, message, next=None):
        self.message = message
        self.next = next

@app.errorhandler(ErrorMessage)
def info_handler(error):
    flash(error.message)
    if error.next == None:
        return redirect("/")
    else:
        return redirect(error.next)