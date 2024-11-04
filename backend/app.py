from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS here
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

# Conditionally load .env file if not in production
if os.getenv("ENV") != "production":
    load_dotenv()

# MongoDB connection setup
client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
# Connect to the MongoDB database and collection
db = client['SWELAB']
collection = db['Users']
projects = db['Projects']

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
    print(username, password)

    # Insert the credentials into the MongoDB collection
    try:
        collection.insert_one({'username': username, 'password': password})
        # Respond back to the frontend
        return jsonify({'status': 'success', 'message': 'Credentials saved to MongoDB'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)})


# TODO: Connect with front end. Convert to POST
@app.route('/create_project/<projectid>', methods=['GET', 'POST'])
def create_project(projectid):
    # projectid = int(request.get_json().get('projectid'))

    project_already_exists = check_project_exists(projectid)

    if project_already_exists:
        return jsonify({'message': "Can't add project. Project id already in use"})
    else:
        project_doc = {'ID': projectid, 'HW1Units': 0, 'HW2Units': 0, 'Authorized_Users': [], 'Users': []}
        projects.insert_one(project_doc)
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
        projects.update_one(filter_query, join_query)
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
        projects.update_one(filter_query, leave_query)
        return jsonify({'message': f'{user} removed from project {projectid}'})


def get_project(projectid):
    return projects.find_one({'ID': int(projectid)})

def check_project_exists(projectid):
    project = projects.find_one({'ID': projectid})
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
