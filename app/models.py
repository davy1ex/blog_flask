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

    def __repr__(self):
        return "<User>: %s" % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_pic(self, size):
        # email = md5(self.email).hexdigest()
        # print(email)
        # print("\n\nhttps://www.gravatar.com/avatar/{0}?s{1}\n\n".format, size))
        return "https://www.gravatar.com/avatar/{0}?s={1}".format(md5(self.email.encode('utf-8')).hexdigest(), size)
