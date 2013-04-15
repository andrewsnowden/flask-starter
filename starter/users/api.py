from ..utils.api import JsonResource
from .. import api, db
from flask.ext.login import current_user
from flask.ext.security.utils import encrypt_password
from flask import request


class User(JsonResource):
    def get(self):
        return current_user.dict()

    def put(self):
        user = request.required_dict("user")

        password = user.optional("password")

        if password:
            current_user.password = encrypt_password(password)

        db.session.commit()

        return {
            "status": 200,
            "message": "User updated"
        }

api.add_resource(User, "/users/me")
