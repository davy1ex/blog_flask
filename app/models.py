# СДЕЛАЙ, БЛЯДЬ, МИГРАЦИОННУЮ БД
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    about = db.Column(db.String(512))
    post = db.relationship("Post", backref="master", lazy="dynamic")

    def __repr__(self):
        return "<User>: %s" % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def change_username(self, new_username):
        self.username = new_username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.String(10000))
    comment = db.relationship("Comment", backref="post", lazy="dynamic")

    def __repr__(self):
        return "<Post: %s>" % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author = db.Column(db.String(64))
    email = db.Column(db.String(64))
    body = db.Column(db.String(140))
    datetime = db.Column(db.DateTime(), default=datetime.now)
    answer = db.relationship("Answer", backref="comment", lazy="dynamic")

    def __repr__(self):
        return "<Comment: %s>" % self.body


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    author = db.Column(db.String(140))
    email = db.Column(db.String(64))
    body = db.Column(db.String(140))
    datetime = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return "<Answer: %s>" % self.body
