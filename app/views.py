# ДОБАВИТЬ ОГРАНИЧЕНИЯ НА ВВОД В КОММЕНТАХ
# ДОБАВИТЬ УДАЛЕНИЕ ФОТО ОТ УДАЛЁННЫХ ПОСТОВ/НОРМАЛЬНУЮ СИСТЕМУ ХРАНЕНИЯ ФОТО
import os
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from app.models import User, Post, Comment
from app.forms import RegForm, LoginForm, ProfileSettingsForm, TextEditorForm, AddCommentForm

admin_username = "admin"


@app.route("/admin", methods=["GET", "POST"])
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
    return redirect("/")


@app.route("/")
@app.route("/index")
def index():
    posts = Post.query.filter_by(master=User.query.filter_by(username=admin_username).first()).all()

    return render_template("index/index.html", posts=posts)


@app.route("/settings/profile", methods=["POST", "GET"])
@login_required
def settings_profile():
    form = ProfileSettingsForm()
    # user = current_user
    # if form.validate_on_submit():
    #     if form.username.data != "":
    #         if User.query.filter_by(username=form.username.data).first() is None:
    #             current_user.change_username(form.username.data)
    #             db.session.commit()

    #     if form.about.data != "":
    #         current_user.change_about(form.about.data)
    #         db.session.commit()
    return render_template("settings/profile.html", form=form)


@app.route("/add_post", methods=["GET", "POST"])
@login_required
def add_post():
    form = TextEditorForm()
    if form.validate_on_submit():

        if form.text != "":
            post = Post(master=current_user, body=form.text.data, title=form.title.data)

            db.session.add(post)
            db.session.commit()
            post = Post.query.filter_by(title=form.title.data).first()
            os.mkdir(os.path.join(os.getcwd(), "app", "static", "img", str(post.id)))

            if "file" not in request.files:
                return redirect(url_for("add_post"))

            file = request.files["file"]

            if file.filename == "":
                return redirect(url_for("add_post"))

            # filename = file.filename # пофиксить безопасные имена при сохранении        
            file.save(os.path.join(os.getcwd(), "app", "static", "img", str(post.id), "img.jpeg"))

            return redirect(url_for("index"))

    return render_template("editor.html", form=form)


@login_required
@app.route("/remove_post/<id>")
def remove_post(id):
    post = Post.query.filter_by(id=id).first()
    os.system("rm -rf " + os.path.join("app", "static", "img", id))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/post_<id>", methods=["GET", "POST"])
def post(id):
    form = AddCommentForm()
    post = Post.query.filter_by(id=id).first_or_404()

    if form.validate_on_submit():
        if request.form["submit"] == "Ok":
            comment = Comment(author=form.author.data, email=form.email.data, body=form.body.data, post=post)
            db.session.add(comment)
            db.session.commit()

            # return redirect(url_for("post", id=id))

    comments = Comment.query.filter_by(post=post).all()
    # comments = [
    #    {
    #         "author": "VinniePoh",
    #         "body": "Нормально...",
    #         "email": "vinniepoh@gmail.com"
    #     },

    #     {
    #         "author": "Sherlock Holmes",
    #         "body": "Где мой кокс?",
    #         "email": "SH@gmail.com"
    #     },

    #     {
    #         "author": "Krosh",
    #         "body": "Ёжик, ты где, блядь?",
    #         "email": "kicoric777@gmail.com"
    #     }
    # ]

    return render_template("index/post.html", post=post, form=form, comments=comments)
