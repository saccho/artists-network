import sys
import json
import settings
from copy import deepcopy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

client_id = settings.client_id
client_secret = settings.client_secret
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = Spotify(client_credentials_manager=client_credentials_manager)

class ArtistsNetwork():
    def __init__(self):
        self.genres = {}
        genre_list = ['metal', 'hard', 'progressive', 'rock',
                      'indie', 'pop', 'anime', 'idol', 'denpa', 'dance',
                      'funk', 'hawaiian', 'jawaiian', 'shibuya', 'reggae',
                      'r&b', 'fusion', 'city', 'jazz']
        max_value = 240
        min_value = 0.1
        step = (max_value - min_value) / (len(genre_list) - 1)
        value_list = [round(min_value + (i * step), 2) for i in range(len(genre_list))]
        for genre, value in zip(genre_list, value_list):
            self.genres[genre] = value

    def get_genres(self):
        return self.genres

    def search_artist_from_name(self, source_artist_name, market):
        artists = {
            'err_msg': '',
            'items': []
        }
        artist_search_results = spotify.search(q=source_artist_name, market=market,
                                               type='artist', limit=15)
        if len(artist_search_results['artists']['items']) == 0:
            artists['err_msg'] = 'Artist not found'
            return artists
        else:
            pass

        artist = {}
        for artist_search_result in artist_search_results['artists']['items']:
            artist['name'] = artist_search_result['name']
            artist['id'] = artist_search_result['id']
            try:
                artist['image'] = artist_search_result['images'][1]['url']
            except IndexError:
                artist['image'] = ''
            artists['items'].append(deepcopy(artist))
        return artists

    def search_related_artists(self, artist_id):
        self._search_artist_from_id(artist_id)
        related_artists = {
            'source': {
                'name': self.artist_name,
                'popularity': self.artist_popularity,
                'genre': self.artist_genres,
                'id': self.artist_id,
                'image': self.artist_image
            },
            'related': []
        }

        related_artist_search_results = spotify.artist_related_artists(artist_id)

        related_artist = {}
        for artist in related_artist_search_results['artists']:
            related_artist['name'] = artist['name']
            related_artist['popularity'] = artist['popularity']
            related_artist['genre'] = self._genres_to_value(artist['genres'])
            related_artist['id'] = artist['id']
            try:
                related_artist['image'] = artist['images'][1]['url']
            except IndexError:
                related_artist['image'] = ''
            related_artists['related'].append(deepcopy(related_artist))
        return related_artists

    def search_artist_albums(self, artist_id):
        albums = {
            'album': [],
            'single': []
        }
        album = {}
        single = {}
        album_search_results = spotify.artist_albums(artist_id)
        for album_search_result in album_search_results['items']:
            if album_search_result['album_type'] == 'album':
                album['name'] = album_search_result['name']
                album['release_date'] = album_search_result['release_date']
                album['spotify_url'] = album_search_result['external_urls']['spotify']
                try:
                    album['image'] = album_search_result['images'][1]['url']
                except IndexError:
                    album['image'] = ''
                albums['album'].append(deepcopy(album))
            else:
                single['name'] = album_search_result['name']
                single['release_date'] = album_search_result['release_date']
                single['spotify_url'] = album_search_result['external_urls']['spotify']
                try:
                    single['image'] = album_search_result['images'][1]['url']
                except IndexError:
                    single['image'] = ''
                albums['single'].append(deepcopy(single))
        return albums

    def _genres_to_value(self, artist_genres):
        if len(artist_genres) == 0:
            return 0
        else:
            count_genres = {}
            genre_values = []
            artist_genres = ','.join(artist_genres).replace('-', ',').replace(' ', ',')
            for genre, value in self.genres.items():
                if artist_genres.count(genre):
                    genre_value = artist_genres.count(genre) * value
                    count_genres[genre] = artist_genres.count(genre)
                    genre_values.append(genre_value)
            try:
                return round(sum(genre_values) / sum(count_genres.values()), 2)
            except ZeroDivisionError:
                return 0

    def _search_artist_from_id(self, artist_id):
        artist_search_results = spotify.artist(artist_id)
        self.artist_name = artist_search_results['name']
        self.artist_popularity = artist_search_results['popularity']
        self.artist_genre = artist_search_results['genres']
        self.artist_genres = self._genres_to_value(self.artist_genre)
        self.artist_id = artist_search_results['id']
        try:
            self.artist_image = artist_search_results['images'][1]['url']
        except IndexError:
            self.artist_image = ''
