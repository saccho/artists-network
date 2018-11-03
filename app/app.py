from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from artists_network import ArtistsNetwork
app = Flask(__name__)
CORS(app)

an = ArtistsNetwork()

@app.route("/")
def main_page():
    artists = an.get_artists('Sheena ringo')
    return artists

if __name__ == "__main__":
    app.run(debug=True)
