from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# MongoDB connection setup
uri = "mongodb+srv://member:memberPass@cluster0.ccbhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the MongoDB database and collections
db = client['SWELAB']
users_collection = db['Users']
projects_collection = db['Projects']

app = Flask(__name__, static_folder='../frontend/build/static', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Constants for encryption
N = 4  # Constant value for shifting characters
D = 1  # Direction multiplier

# Encryption function for password hashing
def encrypt(inputText, N, D):
    revText = inputText[::-1]  # Reverse

    encryptedText = ""
    for char in revText:
        ascii_value = ord(char)

        if ascii_value not in (32, 33):  # " " or "!"
            # Shift the character by N positions in the direction D
            new_ascii = ascii_value + (N * D)

            # Ensure the new ASCII is ok(34 to 126)
            if new_ascii > 126:
                new_ascii = 34 + (new_ascii - 127)
            elif new_ascii < 34:
                new_ascii = 126 - (33 - new_ascii)

            encryptedText += chr(new_ascii)
        else:
            encryptedText += char

    return encryptedText

@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users_collection.find_one({'username': username}):
        return jsonify({'status': 'error', 'message': 'Username already exists'})
    
    encrypted_password = encrypt(password, N, D)
    users_collection.insert_one({'username': username, 'password': encrypted_password})
    return jsonify({'status': 'success', 'message': 'User signed up successfully'})

@app.route('/sign_in', methods=['POST'])
def sign_in():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    encrypted_password = encrypt(password, N, D)
    user = users_collection.find_one({'username': username, 'password': encrypted_password})
    if user:
        return jsonify({'status': 'success', 'message': 'Signed in successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Incorrect username or password'})

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
