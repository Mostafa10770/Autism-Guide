from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
# Set the secret key. Make sure it's a complex and unique string.
app.secret_key = b"\xa3\xc8\xb7\xb5\xc1E\x16\xd4\x05\x86\xe4\xa1h\x8b\xbd\xbf\t?\xd2\xe4v\x91\x82Z"

users_file = os.path.join(os.path.dirname(__file__), 'data', 'users.json')

# Read users from JSON file
def read_users():
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            return json.load(file)
    return []

# Write users to JSON file
def write_users(users):
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    users = read_users()
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    if user:
        session['username'] = user['username']  # Set session
        return redirect(url_for('home'))
    else:
        return jsonify({'message': 'Invalid credentials', 'is_user': False}), 400

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    users = read_users()
    if any(user['username'] == username for user in users):
        return jsonify({'message': 'Username already exists'}), 400
    users.append({'username': username, 'password': password})
    write_users(users)
    return jsonify({'message': 'Registration successful'})

if __name__ == '__main__':
    app.run(debug=True)
