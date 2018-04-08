from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    birthday = db.Column(db.String(255), nullable=False)
    register_time = db.Column(db.String(20), nullable=False)