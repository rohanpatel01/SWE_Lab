from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Conditionally load .env file if not in production
if os.getenv("ENV") != "production":
    load_dotenv()

# MongoDB connection setup
uri = "mongodb+srv://member:memberPass@cluster0.ccbhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
# client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
# Connect to the MongoDB database and collections
db = client['SWELAB']
users_collection = db['Users']
projects_collection = db['Projects']

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static files
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_url_path, path)

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


# TODO: Connect with front end. Convert to POST
@app.route('/create_project/<projectid>', methods=['GET', 'POST'])
def create_project(projectid):
    # projectid = int(request.get_json().get('projectid'))

    project_already_exists = check_project_exists(projectid)

    if project_already_exists:
        return jsonify({'message': "Can't add project. Project id already in use"})
    else:
        project_doc = {'ID': projectid, 'HW1Units': 0, 'HW2Units': 0, 'Authorized_Users': [], 'Users': []}
        projects_collection.insert_one(project_doc)
        return jsonify({'message': 'Project created'})


# TODO: Connect with front end. Convert to POST
@app.route('/join_project/<user>/<projectid>', methods=['GET', 'POST'])
def join_project(user, projectid):
    # data = request.get_json()
    # user = data.get('username')
    # projectid = data.get('projectid')
    projectid = int(projectid)
    project = get_project(projectid)
    if check_user_authorized(user, project) and not check_user_in_project(user, project):
        # logic to add user to project and/or project to the user
        filter_query = {'ID': projectid}
        join_query = {'$push': {'Users': user}}
        projects_collection.update_one(filter_query, join_query)
        return jsonify({'message': "user added"})
    else:
        # logic telling frontend that user is not authorized
        return jsonify({'message': 'user already in project or not authorized'})
    

# TODO: Connect with front end. Convert to POST
@app.route('/leave_project/<user>/<projectid>', methods=['GET', 'POST'])
def leave_project(user, projectid):
    # data = request.get_json()
    # username = data.get('username')
    # projectid = data.get('projectid')
    projectid = int(projectid)
    project = get_project(projectid)
    print(project)
    # Check if user is in project
    if not check_user_in_project(user, project):
        return jsonify({'message': 'User already not in project'})
    else:
        filter_query = {'ID': projectid}
        leave_query = {'$pull': {'Users': user}}
        projects_collection.update_one(filter_query, leave_query)
        return jsonify({'message': f'{user} removed from project {projectid}'})


def get_project(projectid):
    return projects_collection.find_one({'ID': int(projectid)})

def check_project_exists(projectid):
    project = projects_collection.find_one({'ID': projectid})
    if project:
        return True
    return False

def check_user_in_project(user: str, project) -> bool:
    if not project:
        print("no project with id found")
        return False
    if user in project["Users"]:
        return True
    else:
        return False

# Checks if users is authorized to join a project
def check_user_authorized(user: str, project) -> bool:
    if not project:
        print("no project with id found")
        return False
    if user in project["Authorized_Users"]:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(host='localhost', debug=True)

client.close()
