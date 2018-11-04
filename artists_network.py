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
        self.max_value = 240
        self.min_value = 0.1
        step = (self.max_value - self.min_value) / (len(genre_list) - 1)
        value_list = [round(self.min_value + (i * step), 2) for i in range(len(genre_list))]
        for genre, value in zip(genre_list, value_list):
            self.genres[genre] = value

    def _search_artist_from_name(self, source_artist_name):
        artists = {
            'err_msg': '',
            'items': []
        }
        for market in ['US', 'JP']:
            artist_search_results = spotify.search(q=source_artist_name, market=market, type='artist')
            if len(artist_search_results['artists']['items']) != 0:
                break
            else:
                artists['err_msg'] = 'Artist not found'
        if len(artists['err_msg']) != 0:
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

    def _search_related_artists(self, artist_id):
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

    def get_genres(self):
        return self.genres

    def get_artists(self, source_artist_name):
        '''
        param:
            source_artist_name: string
        '''
        artists = self._search_artist_from_name(source_artist_name)
        return artists

    def get_related_artists(self, source_artist_id):
        '''
        param:
            source_artist_id: string
        '''
        artists = self._search_related_artists(source_artist_id)
        return artists

