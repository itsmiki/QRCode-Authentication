from . import db
from flask_login import UserMixin


class LoginTokens(db.Model):
    session = db.Column(db.String(150), primary_key=True)
    loginToken_jwt = db.Column(db.String(10000))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    accountId = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

