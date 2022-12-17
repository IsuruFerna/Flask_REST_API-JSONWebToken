from flask import Flask, request, make_response, jsonify
import jwt #json web token
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.args.get('token') #htttp://127.0.0.1:5000/route?token=blablabla

    if not token:
      return jsonify({'message': 'Token is missing!'}), 403

    try:
      date = jwt.decode(token, app.config['SECRET_KEY'])
    except:
      return jsonify({'message': 'Token is missing or invalid'}), 403

    return f(*args, **kwargs)
  
  return decorated


@app.route('/unprotected')
def unprotected():
  return jsonify({'message': 'Anyone can view this'})

@app.route('/protected')
@token_required
def protected():
  return jsonify({'message': 'This is only available for people with valid token'})

@app.route('/login')
def login():
  auth = request.authorization

  if auth and auth.password == 'password':
    token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

    return jsonify({'token' : token}) #python 3 or above
    # return jsonify({'token' : token.decode('UTF-8')})

  return make_response('Could not Varify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

if __name__ == '__main__':
  app.run(debug=True)