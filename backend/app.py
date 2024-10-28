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


# Don't serve files from flask
@app.route('/')
def home():
    return jsonify(message="Flask api is running"), 200


# Route to handle credentials submission
@app.route('/submit_credentials', methods=['POST'])
def submit_credentials():
    # Get the JSON data sent from React
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Insert the credentials into the MongoDB collection
    try:
        collection.insert_one({'username': username, 'password': password})
        # Respond back to the frontend
        return jsonify({'status': 'success', 'message': 'Credentials saved to MongoDB'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='localhost', debug=True)

client.close()