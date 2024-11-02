from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS here
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# MongoDB connection setup
client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))

# Connect to the MongoDB database and collection
db = client['SWELAB']
collection = db['Users']

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)  # Enable CORS for all routes


@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_url_path, path)


# Route to handle credentials submission
@app.route('/submit_credentials', methods=['POST'])
def submit_credentials():
    # Get the JSON data sent from React
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print("collections:", db.list_collection_names)
    print(username, password)

    # Insert the credentials into the MongoDB collection
    try:
        collection.insert_one({'username': username, 'password': password})
        # Respond back to the frontend
        return jsonify({'status': 'success', 'message': 'Credentials saved to MongoDB'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Route to handle user creation
@app.route('/create_user', methods=['POST'])
def create_user():
    # Get the JSON data sent from React
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    #TODO: Encrypt pass word and then query database for existing user.
    #TODO: If no existing user from database send write instruction to database and success to react.
    #TODO: If existing user, do not write to database and return existing user message

    return

# Encrypt password before querying or storing in database
def encrypt_password(password:str) -> str:
    #TODO: Complete with hashing or some encryption method
    pass


if __name__ == '__main__':
    app.run(host='localhost', debug=True)

client.close()
