from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pqXjNHHNSsiGLyNB9OdyhfOFQMoEn5lZ55mOoMsbRsE'

# Sample user database
users = {
    'Lecturer': 'abcd'
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
        except Exception as e:
            print(e)
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data["username"] or not data["password"]:
        return jsonify({'message': 'Could not verify'}), 401

    if data["username"] in users and users[data["username"]] == data["password"]:
        token = jwt.encode({'username': data["username"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=300)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not "username" in data.keys() or not "password" in data.keys():
        return jsonify({'message': 'Missing data'}), 401
    try:
        if data["username"] in users.keys():
            return jsonify({'message':'username exists'}), 401
        users[data["username"]] = data["password"]
        return jsonify({'status':'Success'})
    except:
        return jsonify({'message': 'Can not register this user'}), 401    

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Welcome!'})

if __name__ == '__main__':
    app.run(debug=True)
