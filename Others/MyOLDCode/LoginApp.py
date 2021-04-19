from flask import Flask, make_response, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def login():
    if request.authorization and request.authorization.password=='password':
        return '<h1>You have Logged in!</>'
    return make_response("Login is Failed", 401)

if __name__ == '__main__':
    app.run(debug=True)
