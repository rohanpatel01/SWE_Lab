from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS here
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# MongoDB connection setup
uri = "mongodb+srv://member:memberPass@cluster0.ccbhc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the MongoDB database and collection
db = client['SWELAB']
collection = db['Users']

app = Flask(__name__, static_folder='../fronend/build/static', static_url_path='/')
CORS(app)  # Enable CORS for all routes

# Render the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("index.html")

# Render the main page
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         return redirect("/")
#     else:
#         return render_template("index.html")

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve_react(path):
#     print(f"Path requested: {path}")
#     # Check if the path exists in the build folder (static assets like JS, CSS, images)
#     if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#         return send_from_directory(app.static_folder, path)
#     else:
#         # Serve index.html for all unknown paths (this is where React takes over)
#         return send_from_directory(app.static_folder, 'index.html')


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