from flask import Flask, redirect, render_template, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS here
import os

app = Flask(__name__, static_folder='../fronend/build/static', static_url_path='/')
CORS(app)  # Enable CORS for all routes

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
    
    # Write the credentials to a file
    with open('credentials.txt', 'a') as f:
        f.write(f"Username: {username}, Password: {password}\n")
    
    # Respond back to the frontend
    return jsonify({'status': 'success', 'message': 'Credentials saved'})

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

