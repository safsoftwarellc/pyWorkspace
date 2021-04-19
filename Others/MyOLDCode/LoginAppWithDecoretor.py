from flask import Flask, make_response, jsonify, request
from functools import wraps

app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def decorator(*args, **kargs):
        if request.authorization and request.authorization.password=='password':
            return f(*args, **kargs);
        return make_response("Login is Failed", 401, {'WWW-Authenticate':'Basic-Realm="Login Required"'})
        
    return decorator


@app.route('/', methods=['GET'])
@login_required
def login():
    return '<h1>Just Logged In!</h1>'
    
@app.route('/nologin', methods=['GET'])
def no_login():
    return '<h1>Without LogIn!</h1>'
    
if __name__ == '__main__':
    app.run(debug=True)
