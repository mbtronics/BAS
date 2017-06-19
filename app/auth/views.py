from . import auth
from .. import db
from ..usermodels import User
from flask import abort

@auth.route('/verify/<int:code>')
def verify(code):
    user = User.query.filter(User.code==code).first()

    if not user or not user.authorized:
        abort(401)

    return "hello " + user.name