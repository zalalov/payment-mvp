from flask_restful import Resource
from flask import request, abort, jsonify, url_for, make_response, g

from models import User
from users import create_user
from decorators import login_required


class Events(Resource):
    @login_required
    def get(self, *args, **kwargs):
        return {'data': [event.to_json() for event in g.current_user.events]}, 200
