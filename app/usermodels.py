from . import db

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    authorized = db.Column(db.Boolean(), default=False, nullable=False)