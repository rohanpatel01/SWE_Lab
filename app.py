from flask import Flask, request, jsonify

app = Flask(__name__)

users = [{"username": "user1", "password": "password123"}]  

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the username already exists
    if any(user['username'] == username for user in users):
        return jsonify({"message": "Username already exists"}), 400

    # Add new user if the username doesn't exist
    users.append({"username": username, "password": password})
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid username or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
