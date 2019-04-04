from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from app.models import User
from app.forms import RegForm, LoginForm


@app.route("/reg", methods=["GET", "POST"])
def registratoin():
    form = RegForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Success.")
            return redirect("/login")
        else:
            flash("This username already registered.")
        return redirect("/")
    return render_template("authorize/reg.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Now you in our system.")
        else:
            flash("User with this login and password not found")
        return redirect("/")
    return render_template("authorize/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index/index.html")