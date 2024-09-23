from flask import Flask, redirect, render_template, request

app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        return redirect("/")

    else:

        return render_template("index.html")