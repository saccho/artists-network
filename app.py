import os
from flask import Flask, jsonify
from flask_cors import CORS
from artists_network import ArtistsNetwork

app = Flask(__name__)
CORS(app)

an = ArtistsNetwork()

@app.route('/')
def index():
    return 'artists-network-api'

@app.route('/source-artists/<market>/<artist_name>', methods=['GET'])
def search_source_artists(artist_name, market):
    source_artist = jsonify(an.get_artists(artist_name, market))
    source_artist.status_code = 200
    return source_artist

@app.route('/related-artists/<artist_id>', methods=['GET'])
def search_related_artists(artist_id):
    related_artist = jsonify(an.get_related_artists(artist_id))
    related_artist.status_code = 200
    return related_artist

@app.route('/genres', methods=['GET'])
def genres():
    genres = jsonify(an.get_genres())
    genres.status_code = 200
    return genres

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
