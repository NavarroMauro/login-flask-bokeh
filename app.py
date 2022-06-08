from bokeh.util import token
from bokeh.client import pull_session
from bokeh.embed import server_session
import os
from flask import Flask, render_template, request, redirect
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, db, login
from bokeh.embed import server_document

script = server_document("https://onrtools.staging.quantyoo.dev/liferadio")


SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.secret_key = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
login.init_app(app)
login.login_view = "login"


@app.before_first_request
def create_all():
    db.create_all()


# @app.route("/dashboard")
# @login_required
# def dashboard():
    # s_id = token.generate_session_id()
    # return redirect("http://<bokeh-server-addr>:<port>/?bokeh-session-id={}".format(s_id), code=302)
    # return render_template("dashboard.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return  render_template('dashboard.html', my_script=script)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form["email"]
        user = UserModel.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form["password"]):
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        if UserModel.query.filter_by(email=email).first():
            return "Email already Present"

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/")
@login_required
def index():
    return redirect("/login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
