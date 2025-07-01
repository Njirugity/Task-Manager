from flask import Flask, request,jsonify
from flask_bcrypt import Bcrypt
from storage.db import Db

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = Db()
@app.route('/')
def index ():
    return 'Connected'

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
    else:
        return jsonify({"message":"Login successfull"})
   


#Task Routes
# @app.route('/tasks', methods=["POST"])
# def create_task():
#     pass  

# @app.route('/task', methods=["GET"])
# def get_task():
#     pass


if __name__ == "__main__":
    app.run(debug=True)