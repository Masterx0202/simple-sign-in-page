from flask import Flask, render_template, request, redirect, url_for
import pymongo

app = Flask(__name__)
# enter youre database
client = pymongo.MongoClient("DATABASE")
db = client.userlistfirstdatabaseproject

dbuserdata = db.userdata

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("action") == "signin":
            return redirect(url_for("insert"))
        elif request.form.get("action") == "login":
            return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/signin", methods=["GET", "POST"])
def insert():
    if request.method == "POST":
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        existing_user = dbuserdata.find_one({"name": name})
        if existing_user:
            return "User already exists. Please log in."
        dbuserdata.insert_one({"name": name, "password": password})
        return redirect(url_for("signin_success", name=name))
    return render_template("signin.html")

@app.route("/signin_success")
def signin_success():
    name = request.args.get("name", "")
    return render_template("user.html", name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        user = dbuserdata.find_one({"name": name, "password": password})
        if user:
            return render_template("sucess.html", name=name)
        return "Invalid credentials. Please try again."
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
