from flask import render_template
from app import db, app


@app.errorhandler(404)
def not_found():
    return "Uups, this is 404 error page..."