from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/welcome")
def welcome():
    return render_template("Welcome.html")
@app.route("/thankYou")
def thanks():
    return render_template("thankYou.html")
@app.route("/Home")
def home():
    return render_template("homePage.html")
@app.route("/input")
@app.route("/")
def index():
    return render_template("Welcome.html")



def inputs():
    return render_template("inputPageInitial.html")
@app.route("/submit", methods=["POST"])

def submit():
    favorite_artist_0 = request.form.get("favoriteArtist0")
    favorite_artist_1 = request.form.get("favoriteArtist1")
    favorite_artist_2 = request.form.get("favoriteArtist2")
    favorite_song_0 = request.form.get("favoriteSong0")
    favorite_song_1 = request.form.get("favoriteSong1")
    favorite_song_2 = request.form.get("favoriteSong2")
    genre = request.form.get("genre")
    return render_template("thankYou.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)