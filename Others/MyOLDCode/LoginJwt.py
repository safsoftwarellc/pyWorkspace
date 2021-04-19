from flask import Flask, make_response, jsonify, request
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY']='donotdisclose'

def login_required(f):
    @wraps(f)
    def decorator(*args, **kargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'No token found!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            return jsonify({'message':'Invalid token'}), 403

        return f(*args, **kargs)

    return decorator


@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message':'This is Protected API'})

@app.route('/unprotected', methods=['GET'])
def unprotected():
    return jsonify({'message':'This is Unprotected API'})

@app.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth.username=='Sunil' and auth.password=='password':
        token=jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})
    return make_response('Could not verify the account!', 401, {'WWW-Authenticate':'Basic-realm:"Login Required"'})



if __name__ == '__main__':
    app.run(debug=True)