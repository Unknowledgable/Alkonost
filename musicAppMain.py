from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/Home")
def home():
    return render_template("homePage.html")
@app.route("/UserPreferences")
def preferences():
    return render_template("PreferenceUpdate.html")
@app.route("/Login")
def login():
    return render_template("userLogin.html")
@app.route("/profile")
def profile():
    return render_template("userProfile.html")
@app.route("/Splash")
def splash():
    return render_template("Welcome.html")

@app.route("/submit", methods=["POST"])

def submit():
    favorite_artist_0 = request.form.get("favoriteArtist0")
    favorite_artist_1 = request.form.get("favoriteArtist1")
    favorite_artist_2 = request.form.get("favoriteArtist2")
    favorite_song_0 = request.form.get("favoriteSong0")
    favorite_song_1 = request.form.get("favoriteSong1")
    favorite_song_2 = request.form.get("favoriteSong2")
    genre = request.form.get("genre")
    return render_template("userLogin.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)