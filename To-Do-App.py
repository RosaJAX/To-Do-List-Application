from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.config["SECRET_KEY"] = "your_secret_key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user["_id"]))
    return None

@app.route('/')
@login_required
def home():
    tasks = mongo.db.tasks.find({"user_id": ObjectId(current_user.id)})
    return render_template('index.html', tasks=tasks)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({"username": username, "password": hashed_password})
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({"username": username})
        if user and bcrypt.check_password_hash(user['password'], password):
            login_user(User(str(user["_id"])))
            return redirect(url_for('home'))
        flash('Login failed. Check your username and/or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = mongo.db.tasks.find({"user_id": ObjectId(current_user.id)})
    return jsonify([task for task in tasks])

@app.route('/tasks', methods=['POST'])
@login_required
def add_task():
    task = request.json
    task['user_id'] = ObjectId(current_user.id)
    result = mongo.db.tasks.insert_one(task)
    return jsonify({"_id": str(result.inserted_id)}), 201

@app.route('/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": ObjectId(current_user.id)})
    if result.deleted_count:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"message": "Task not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
