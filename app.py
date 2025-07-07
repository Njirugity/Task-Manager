from flask import Flask, request,jsonify, make_response, g
from flask_bcrypt import Bcrypt
from storage.db import Db
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'secret_key'
db = Db()
CORS(app)
@app.route('/')
def index ():
    return 'Connected'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Authentication Token is missing!"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.user_id = data['user_id'] 
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
        except Exception as e:
            return jsonify({"message": f"Token error: {str(e)}"}), 401
        return func(*args, **kwargs)
    return decorated

# User routes
@app.route('/register', methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if not all ([username, email, password]):
        return jsonify({"message":"Missing  Username, Email, or password"}), 400
    
    try:
        new_user = db.add_user(username, email, hashed_password)
        return jsonify({"message":"Registration successfull", "user_id":new_user.id})
    
    except Exception as e:
        import sqlalchemy.exc
        if isinstance(e, sqlalchemy.exc.IntegrityError):
            return jsonify({"message": "Username or email already exists"}), 409
        return jsonify({"message": f"Error registering user: {str(e)}"}), 500
    
@app.route('/login', methods=["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not all([username, password]):
        return jsonify({"message": "Missing username or password"}), 400
    
    user = db.get_user_by_username(username)
    
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message":"Invalid credentials"}), 401
    token = jwt.encode({
        'user_id': user.id
    },
        app.config['SECRET_KEY'],
        algorithm="HS256")
    return jsonify({"message": "Logged in successfully", "token": token}), 200
   


#Task Routes
@app.route('/tasks', methods=["POST"])
@token_required
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get("description")
    user_id = g.user_id

    new_task = db.add_task(title, description, user_id)
    return jsonify({"message":"Successfull", "user_id":user_id})

@app.route('/tasks', methods=['GET'])
@token_required
def get_task():
    user_id = g.user_id
    task = db.get_task(user_id)
    return jsonify(task), 200

@app.route("/tasks/<task_id>", methods=["GET"])
@token_required
def get_single_task(task_id):
    user_id = g.user_id
    try:
        task = db.get_single_task(task_id, user_id)

        if task:
            return jsonify(task)
        else:
            return jsonify({"message": "Task not found or unauthorized"}), 404

    except Exception as e:
        app.logger.error(f"Error retrieving task {task_id} for user {user_id}: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
@app.route("/tasks/<task_id>", methods=["PUT"])
@token_required
def update_tasks(task_id):
    user_id = g.user_id
    data = request.get_json()
    if not data:
        return jsonify({"message":"Body must contain data to update"}), 400
    update_task = db.update_task(task_id, user_id, data)
    if update_task:
        return jsonify (update_task.to_dict()), 200
    else:
        return jsonify({"message":"Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["DELETE"])
@token_required
def delete_task(task_id):
    user_id = g.user_id
    deleted = db.delete_task(task_id, user_id)
    if deleted:
        return "", 204
    else:
        return jsonify({"message":"Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)