from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# MongoDB connection setup
uri = "mongodb+srv://member:memberPass@cluster0.ccbhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
# client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
# Connect to the MongoDB database and collections
db = client['SWELAB']
users_collection = db['Users']
projects_collection = db['Projects']
resources_collection = db['Resources']

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

@app.route('/fetchData', methods=['POST'])
def fetch_data():
    data = request.get_json()
    projectID = data.get('projectID')
    print("ProjectID recieved: ", projectID)

    HW_Set_1 = resources_collection.find_one({'Name': "HW_Set_1"})
    HW_Set_2 = resources_collection.find_one({'Name': "HW_Set_2"})

    HwSet1_available = HW_Set_1.get('Availability')
    HwSet1_capacity = HW_Set_1.get('Capacity')

    HwSet2_available = HW_Set_2.get('Availability')
    HwSet2_capacity = HW_Set_2.get('Capacity')

    return jsonify({
        'status': 'success', 'message': 'Fetch Data successful',
        'HwSet1_available': HwSet1_available,
        'HwSet1_capacity': HwSet1_capacity,
        'HwSet2_available': HwSet2_available,
        'HwSet2_capacity': HwSet2_capacity
        })

@app.route('/sign_up', methods=['POST'])
def sign_up():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or username.strip() == "":
        return jsonify({'status': 'error', 'message': 'Invalid Username: Cannot be empty'})
    if not password or password.strip() == "":
        return jsonify({'status': 'error', 'message': 'Invalid Username: Cannot be empty'})

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

    if not username or username.strip() == "":
        return jsonify({'status': 'error', 'message': 'Invalid Username: Cannot be empty'})
    if not password or password.strip() == "":
        return jsonify({'status': 'error', 'message': 'Invalid Password: Cannot be empty'})

    encrypted_password = encrypt(password, N, D)
    print("Username: ", username)
    print("Password", password)
    user = users_collection.find_one({'username': username, 'password': encrypted_password})
    if user:
        return jsonify({'status': 'success', 'message': 'Signed in successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Incorrect username or password'})


# TODO: Implement a unique project ID generator
@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.get_json()
    
     # Check if data is None or missing required fields
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    print(data)
    projectid = data.get('projectid')
    projectName = data.get('projectName')
    projectDescription = data.get('projectDescription')
    projectAuthor = str(data.get('username'))

    if not projectid or not projectName or not projectDescription:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    projectid = int(projectid)
    project_already_exists = check_project_exists(projectid)

    if project_already_exists:
        return jsonify({'status': 'error', 'message': "Can't add project. Project id already in use"})
    else:
        project_doc = {'ID': projectid, 'Project_Name': projectName, 'Project_Description': projectDescription, 'HW1Units': 0, 'HW2Units': 0, 'Authorized_Users': [projectAuthor], 'Users': []}
        projects_collection.insert_one(project_doc)
        return jsonify({'status': 'success', 'message': 'Project created'})
    
@app.route('/fetch_authorized_projects', methods=['POST'])
def fetch_authorized_projects():
    data = request.get_json()
    username = str(data.get('user'))
    print(username)
    if not username:
        return jsonify({'status': 'error', 'message': 'Username is required'}), 400

    try:
        print("Username:", username)
        username = str(username)  # Ensure it's a string
        authorized_projects = list(projects_collection.find(
            {"Authorized_Users": {"$in": [username]}},
            {'_id': 1, 'ID': 1, 'Project_Name': 1}
        ))

        print("Authorized Projects:", authorized_projects)

        # Convert ObjectIds to strings for JSON serialization
        for project in authorized_projects:
            project['_id'] = str(project['_id'])
            # project['ID'] = str(project['ID'])

        return jsonify({'status': 'success', 'authorizedProjects': authorized_projects})
    except Exception as e:
        print("Error finding authorized projects:", str(e))
        return jsonify({'status': 'error', 'message': 'Issue finding projects'}), 500

@app.route('/join_project', methods=['POST'])
def join_project():
    data = request.get_json()

    # Check if data is None or missing required fields
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    user = data.get('username')
    projectid = data.get('projectid')

    if not projectid or not user:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    projectid = int(projectid)
    if not check_project_exists(projectid):
        return jsonify({'status': 'error', 'message': 'Project does not exist'}), 400
    

    projects_collection.update_one(
    {"ID": projectid},  # Filter to locate the specific document
    {"$push": {"Authorized_Users": user}}  # Push the new user to the 'members' array
    )
    return jsonify({'status': 'success', 'message': "user added"})
    
@app.route('/goto_project', methods=['POST'])
def goto_project():
    data = request.get_json()

    # Check if data is None or missing required fields
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    user = data.get('username')
    projectid = data.get('projectid')

    if not projectid or not user:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    projectid = int(projectid)
    if not check_project_exists(projectid):
        return jsonify({'status': 'error', 'message': 'Project does not exist'}), 400
    
    return jsonify({'status': 'success', 'message': "user added"})

# TODO: Connect with front end. Convert to POST
@app.route('/leave_project', methods=['POST'])
def leave_project():
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

@app.route('/CheckOut', methods=['POST'])
def CheckOut():
    data = request.get_json()

    projectID = data.get('projectID')
    hw1_request = int(data.get('HW_Set_1_Request')) if data.get('HW_Set_1_Request') else 0
    hw2_request = int(data.get('HW_Set_2_Request')) if data.get('HW_Set_2_Request') else 0

    if hw1_request < 0 or hw2_request < 0:
        return jsonify({"message": "Invalid request. Cannot request negative values."}), 400

    if hw1_request == 0 and hw2_request == 0:
        return jsonify({"message": "Invalid request. Make sure request values are postive integers."}), 400

    db = client['SWELAB']
    resources_collection = db['Resources']
    projects_collection = db['Projects']
    print("test: ", projectID)
    project = projects_collection.find_one({'ID': int(projectID)})
    project_availabiltiy_HW1 = project.get('HW1Units')
    project_availabiltiy_HW2 = project.get('HW2Units')

    hardWareSet1 = resources_collection.find_one({'Name': 'HW_Set_1'})
    hardWareSet2 = resources_collection.find_one({'Name': 'HW_Set_2'})

    error = False

    # Perform Hardware Set 1 operations
    if hardWareSet1 and hw1_request:
        hw1_availability = int(hardWareSet1.get('Availability'))

        amount_HW1_to_remove = 0
        amount_projectID_to_checkout = 0

        if hw1_request > hw1_availability:
            error = True
            amount_HW1_to_remove = hw1_availability
            amount_projectID_to_checkout = hw1_availability
        else:
            amount_HW1_to_remove = hw1_request
            amount_projectID_to_checkout = hw1_request

        resources_collection.update_one(
            {'Name': "HW_Set_1"},
            {'$set': {'Availability' : hw1_availability - amount_HW1_to_remove}}     # Update operation
        )

        projects_collection.update_one(
            {'ID': projectID},  # Filter criteria
            {'$set': {'HW1Units': project_availabiltiy_HW1 + amount_projectID_to_checkout }}     # Update operation
        )

    # Perform Hardware Set 2 operations
    if hardWareSet2 and hw2_request:
        hw2_availability = int(hardWareSet2.get('Availability'))

        amount_HW2_to_remove = 0
        amount_projectID_to_checkout = 0

        if hw2_request > hw2_availability:
            error = True
            amount_HW2_to_remove = hw2_availability
            amount_projectID_to_checkout = hw2_availability
        else:
            amount_HW2_to_remove = hw2_request
            amount_projectID_to_checkout = hw2_request

        resources_collection.update_one(
            {'Name': "HW_Set_2"},
            {'$set': {'Availability' : hw2_availability - amount_HW2_to_remove}}   
        )

        projects_collection.update_one(
            {'ID': projectID},  
            {'$set': {'HW2Units': project_availabiltiy_HW2 + amount_projectID_to_checkout }}   
        )

    if error:
        return jsonify({"message": "Error. Could not process entire check out value"}), 400
    else:
        return jsonify({"message": "Check Out Successful"}), 200

@app.route('/CheckIn', methods=['POST'])
def CheckIn():
    data = request.get_json()
    projectID = data.get('projectID')
    hw1_request = int(data.get('HW_Set_1_Request')) if data.get('HW_Set_1_Request') else 0
    hw2_request = int(data.get('HW_Set_2_Request')) if data.get('HW_Set_2_Request') else 0

    # print("HW1 Request: " + str(hw1_request) + " HW2 Request: " + str(hw2_request))
    if hw1_request < 0 or hw2_request < 0:
        return jsonify({"message": "Check out value cannot be negative"}), 400

    db = client['SWELAB']
    resources_collection = db['Resources']
    projects_collection = db['Projects']

    project = projects_collection.find_one({'ID': int(projectID)})
    project_availabiltiy_HW1 = project.get('HW1Units')
    project_availabiltiy_HW2 = project.get('HW2Units')


    hardWareSet1 = resources_collection.find_one({'Name': 'HW_Set_1'})
    hardWareSet2 = resources_collection.find_one({'Name': 'HW_Set_2'})

    error = False

    # Perform Hardware Set 1 operations
    # Attempt to check in as many as possible
    if hardWareSet1 and hw1_request:
        hw1_availability = int(hardWareSet1.get('Availability'))
        hw1_capacity = int(hardWareSet1.get('Capacity'))

        amount_HW1_to_add = 0
        amount_projectID_to_checkin = 0

        if hw1_request + hw1_availability <= hw1_capacity:
            amount_HW1_to_add = hw1_request
            amount_projectID_to_checkin = hw1_request
            print("correct")
        else:
            error = True
            amount_HW1_to_add = hw1_capacity - hw1_availability
            amount_projectID_to_checkin = hw1_capacity - hw1_availability


        resources_collection.update_one(
            {'Name': "HW_Set_1"},
            {'$set': {'Availability' : hw1_availability + amount_HW1_to_add}}    
        )

        projects_collection.update_one(
            {'ID': projectID},  
            {'$set': {'HW1Units': project_availabiltiy_HW1 - amount_projectID_to_checkin }}     
        )

    else:
        print("Hardware Set 1 check in could not be completed")


    # Perform Hardware Set 2 operations
    if hardWareSet2 and hw2_request:
        hw2_availability = int(hardWareSet2.get('Availability'))
        hw2_capacity = int(hardWareSet2.get('Capacity'))

        amount_HW2_to_add = 0
        amount_projectID_to_checkin = 0

        if hw2_request + hw2_availability <= hw2_capacity:
            amount_HW2_to_add = hw2_request
            amount_projectID_to_checkin = hw2_request
        else:
            error = True
            amount_HW2_to_add = hw2_capacity - hw2_availability
            amount_projectID_to_checkin = hw2_capacity - hw2_availability

        resources_collection.update_one(
            {'Name': "HW_Set_2"},
            {'$set': {'Availability' : hw2_availability + amount_HW2_to_add}}    
        )

        projects_collection.update_one(
            {'ID': projectID},  
            {'$set': {'HW2Units': project_availabiltiy_HW2 - amount_projectID_to_checkin }}     
        )

    if error:
        return jsonify({"message": "Error. Could not process entire check in value"}), 400
    else:
        return jsonify({"message": "Check In Successful"}), 200



if __name__ == '__main__':
    app.run(host='localhost', debug=True)