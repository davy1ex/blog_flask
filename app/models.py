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

    def change_about(self, new_about):
        self.about = new_about

    def get_pic(self, size):
        return "https://www.gravatar.com/avatar/{0}?s={1}".format(md5(self.email.encode('utf-8')).hexdigest(), size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(256))
    body = db.Column(db.String(1000))

    def __repr__(self):
        return "<Post: %s>" % self.title
