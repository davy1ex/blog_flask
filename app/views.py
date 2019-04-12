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
            user = User(username=form.username.data, email=form.email.data)
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
            return redirect("/")
        else:
            flash("User with this login and password not found")        
    return render_template("authorize/login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/user/<username>")
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            "title": "Как продать гараж?",
            "body":  "Итак, в следующей статье мы рассмотрим то, как продать гараж. А пока что, пожалуйста, перейдите по этой ссылке <a href=go.to:sefjerg;erj;gjrgi;jdg;rjdfgdrjgi;dgdjgkdjgjdfkgjdfl;gdfgjdfgd.com>go.to:sefjerg;erj;gjrgi;jdg;rjdfgdrjgi;dgdjgkdjgjdfkgjdfl;gdfgjdfgd.com</a>",
            "author": user
        },
        
        {
            "title": "Вред конфет",
            "body":  "Всем привет, сегодня я вам объясню почему вы жирное гавно.",
            "author": user
        },

        {
            "title": "цуашоуцщаоуы",
            "body":  "аывавыавыац",
            "author": user
        },
    ]
    return render_template("index/user.html", posts=posts)


@app.route("/")
@app.route("/index")
@login_required
def index():
    if not current_user.is_anonymous:
        return redirect("/user/" + current_user.username)

    return render_template("index/index.html")


