from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "SustosMagnificos_SpookyDooky"
db = SQLAlchemy(app)
DB_DIR ="db_storage"
DB_NAME = "alkonost.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)
LOG_PATH = os.path.join(DB_DIR, "initLog.txt")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(140), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    preferences =db.relationship("UserPreferences", backref="user", uselist=False)
    feedback = db.relationship("UserFeedback", backref="user", lazy=True)

class UserFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    action = db.Column(db.String(25), nullable=False)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entries = db.relationship("PreferenceEntry", backref="preferences", lazy=True)

class PreferenceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preferences_id = db.Column(db.Integer, db.ForeignKey('user_preferences.id'), nullable=False)
    type = db.Column(db.String(10))
    name = db.Column(db.String(200))
    weight = db.Column(db.Integer)

def log(message):
    with open(LOG_PATH, "a") as newLine:
        newLine.write(message + "\n")
    print(message)
#TODO make this require explicit per time admin permission to write
def prepare_db_directory():
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
            log("Made new directory")
        if os.path.exists(DB_PATH):
            log("Database Located, connecting shortly")
        else:
            log("Database not found. creation attempt will proceed shortly")

def init_db():
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    try:
        with app.app_context():
            db.create_all()
            log("all schema have been created or already exist.")
    except Exception as schema_error:
        log(f"Failed to create schema: {schema_error}")
        print("WARNING!: Schema could not be created!")
    return db
def start_database():
    try:
        prepare_db_directory()
        return init_db()
    except Exception as setup_error:
        log(f"Failed to start database:{setup_error}")
        print("WARNING!: there was an error in database startup")
        return None

@app.route("/Home")
def home():
    return render_template("homePage.html")
@app.route("/UserPreferences")
def preferences():
    return render_template("PreferenceUpdate.html")
@app.route("/Login")
def login():
    return render_template("userLogin.html")
@app.route("/Profile")
def profile():
    return render_template("userProfile.html")
@app.route("/Splash")
def splash():
    return render_template("Welcome.html")
@app.route("/")
def root():
    return splash()
@app.route("/submit_preferences", methods=["POST"])
def submit():
    prefs = {
        "favorite_artist_0": request.form.get("favoriteArtist0"),
        "favorite_artist_1": request.form.get("favoriteArtist1"),
        "favorite_artist_2": request.form.get("favoriteArtist2"),
        "favorite_song_0": request.form.get("favoriteSong0"),
        "favorite_song_1":  request.form.get("favoriteSong1"),
        "favorite_song_2": request.form.get("favoriteSong2"),
        "favorite_genre0": request.form.get("genre0"),
        "favorite_genre1": request.form.get("genre1"),
        "favorite_genre2": request.form.get("genre2"),

    }

@app.route("/submit_login", methods=["POST"])
def submit_login():
    if not request.referrer or "Login" not in request.referrer:
        return "invalid Login Attempt", 400
    email = request.form.get("email")
    password = request.form.get("password")

    #TODO: login checker function goes hurr
    if email == "douglas@aklonost.com" and password == "Douglas4Lyfe":
        session["user_id"] = 1
        session["is_guest"] = False
        return redirect("/Home")
    return render_template("userLogin.html", error="you lack cred.")

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    try:
        data = request.get.json()
        title = data.get("title")
        action = data.get("action")
        user_id = session.get("user_id")
        is_guest = session.get("is_guest", True)
        if is_guest:
            guest_user = get_or_create_guest()
            user_id = guest_user.id
        else:
            user_id = session.get("user_id")
            if not user_id:
                return redirect("/Login")
        feedback = UserFeedback(user_id=user_id, title=title, action=action)
        db.session.add(feedback)
        db.session.commit()
        return "OK", 200
    except Exception as e:
        log(f"Feedback submission failed: {e}")
        return "Feedback was not submitted", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)