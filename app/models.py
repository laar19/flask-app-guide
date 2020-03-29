from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), unique=True)
    email       = db.Column(db.String(50))
    password    = db.Column(db.String(94))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    commets     = db.relationship("Comment")

    def __init__(self, username, email, password):
        self.username = username
        self.password = self.__create_password(password)
        self.email    = email

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, crypted_password, password):
        return check_password_hash(crypted_password, password)

class Comment(db.Model):
    __tablename__ = "comments"

    id          = db.Column(db.Integer, primary_key=True)
    text        = db.Column(db.Text())
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"))
