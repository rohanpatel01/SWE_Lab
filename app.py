from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
CORS(app)


uri = "mongodb+srv://member1:memberPass1@cluster0.ccbhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
users = {
    "user": "pass",
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if username in users and users[username] == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if username in users:
        return jsonify({"message": "Username already exists"}), 400

    users[username] = password
    return jsonify({"message": "Sign up successful"}), 201

def connectToMongoDB():
    try:
        client.admin.command('ping')
        print("Connection to MongoDB is established.")
    except Exception as e:
        print(e)

#         hw1_capacity = int(hardWareSet1.get('Capacity'))


@app.route('/CheckIn', methods=['POST'])
def CheckIn():
    connectToMongoDB()
    data = request.get_json()
    projectID = data.get('projectID')
    hw1_request = int(data.get('HW_Set_1_Request')) if data.get('HW_Set_1_Request') else -1
    hw2_request = int(data.get('HW_Set_2_Request')) if data.get('HW_Set_2_Request') else -1

    if hw1_request < 0 or hw2_request < 0:
        return jsonify({"message": "Check out value cannot be negative"}), 400

    db = client['SWELAB']
    resources_collection = db['Resources']
    projects_collection = db['Projects']

    project = projects_collection.find_one({'ID': projectID})
    project_availabiltiy_HW1 = project.get('HW1Units')
    project_availabiltiy_HW2 = project.get('HW2Units')


    hardWareSet1 = resources_collection.find_one({'Name': 'HW_Set_1'})
    hardWareSet2 = resources_collection.find_one({'Name': 'HW_Set_2'})

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
        else:
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

    else:
        print("Hardware Set 2 check in could not be completed")

        
    return jsonify({"message": "Check In Successful"}), 200


@app.route('/CheckOut', methods=['POST'])
def CheckOut():
    connectToMongoDB()
    data = request.get_json()

    projectID = data.get('projectID')
    hw1_request = int(data.get('HW_Set_1_Request')) if data.get('HW_Set_1_Request') else -1
    hw2_request = int(data.get('HW_Set_2_Request')) if data.get('HW_Set_2_Request') else -1

    if hw1_request < 0 or hw2_request < 0:
        return jsonify({"message": "Check out value cannot be negative"}), 400

    db = client['SWELAB']
    resources_collection = db['Resources']
    projects_collection = db['Projects']

    project = projects_collection.find_one({'ID': projectID})
    project_availabiltiy_HW1 = project.get('HW1Units')
    project_availabiltiy_HW2 = project.get('HW2Units')


    hardWareSet1 = resources_collection.find_one({'Name': 'HW_Set_1'})
    hardWareSet2 = resources_collection.find_one({'Name': 'HW_Set_2'})

    # Perform Hardware Set 1 operations
    if hardWareSet1 and hw1_request:
        hw1_availability = int(hardWareSet1.get('Availability'))

        amount_HW1_to_remove = 0
        amount_projectID_to_checkout = 0

        if hw1_request > hw1_availability:
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

    else:
        print("Hardware Set 1 check out could not be completed")



    # Perform Hardware Set 2 operations
    if hardWareSet2 and hw2_request:
        hw2_availability = int(hardWareSet2.get('Availability'))

        amount_HW2_to_remove = 0
        amount_projectID_to_checkout = 0

        if hw2_request > hw2_availability:
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

    else:
        print("Hardware Set 2 check out could not be completed")

        
    return jsonify({"message": "Check Out Successful"}), 200



if __name__ == '__main__':
    app.run(debug=True)