from flask import request
from flask_restplus import Resource

from main.service.auth_helper import Auth
from main.util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth

@api.route('/login')
class UserLogin(Resource):
    """
    User Login resource
    """

    @api.expect(user_auth, validate=True)
    def post(self):
        post_date= request.json
        return Auth.login_user(data=post_date)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @api.doc('Logout a user')
    def post(self):
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)


