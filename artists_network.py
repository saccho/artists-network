import os
import sys
import json
from copy import deepcopy
from conf import client
from conf.color_map import node_cmap
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.client import SpotifyException
import matplotlib.pyplot as plt
import networkx as nx

client_id = client.client_id
client_secret = client.client_secret
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = Spotify(client_credentials_manager=client_credentials_manager)

current_dir = os.path.dirname(__file__)

class ArtistsNetwork():
    def __init__(self, artist_name=None, artist_id=None):
        if artist_name == None and artist_id == None:
            sys.exit('Argument artist_name or artist_id is required.')
        elif artist_id != None:
            self.artist_name = ''
            self.artist_id = artist_id
        else:
            self.artist_name = artist_name
            self.artist_id = ''
            
        self.related_artist_names = []
        self.related_artist_ids = []
        self.related_artist_popularities = []
        self.related_artist_genres = []
        self.related_artist_images = []

        self.genres = {}
        genre_list = ['metal', 'hard', 'progressive', 'rock', 
                      'indie', 'pop', 'anime', 'idol', 'denpa', 
                      'dance', 'r&b', 'reggae', 'funk', 'shibuya', 
                      'fusion', 'city', 'jazz']
        self.max_value = 100
        self.min_value = 20
        step = (self.max_value - self.min_value) / (len(genre_list) - 1)
        value_list = [round(self.max_value - (i * step), 2) for i in range(len(genre_list))]
        for genre, value in zip(genre_list, value_list):
            self.genres[genre] = value

        self.G = nx.Graph()
        
    def search_artist_from_name(self):
        try:
            for market in ['US', 'JP']:
                artist_search_results = spotify.search(q=self.artist_name, market=market, type='artist')
                if len(artist_search_results['artists']['items']) != 0:
                    err_msg = ''
                    break
                else:
                    err_msg = 'Artist not found'
            if len(err_msg) != 0:
                raise ValueError(err_msg)
            else:
                pass
        except ValueError as err:
            sys.exit(err)

        if len(artist_search_results['artists']['items']) == 1:
            artist_index = 0
        else:
            print('-'*50)
            print('Input the index of "{}".'.format(self.artist_name))
            print('-'*50)
            for i, artist_search_result in enumerate(artist_search_results['artists']['items']):
                try:
                    print("[{}] {} - popularity: {}, ImageURL: {}".format(i, artist_search_result['name'],
                        artist_search_result['popularity'], artist_search_result['images'][1]['url']))
                except IndexError:
                    print("[{}] {} - popularity: {}".format(i, artist_search_result['name'],
                        artist_search_result['popularity']))
            print('-'*50)
            artist_index = int(input('Artist Index: '))
        try:
            self.artist_name = artist_search_results['artists']['items'][artist_index]['name']
            self.artist_id = artist_search_results['artists']['items'][artist_index]['id']
            self.artist_popularity = artist_search_results['artists']['items'][artist_index]['popularity']
            self.artist_genre = artist_search_results['artists']['items'][artist_index]['genres']
            self.artist_genres = self.genres_to_value(self.artist_genre)
            try:
                self.artist_image = artist_search_results['artists']['items'][artist_index]['images'][1]['url']
            except IndexError:
                self.artist_image = ''
        except IndexError:
            sys.exit('Input the correct artist name.')

    def search_artist_from_id(self):
        try:
            artist_search_results = spotify.artist(self.artist_id)
        except SpotifyException:
            sys.exit('Artist not found')
        self.artist_name = artist_search_results['name']
        self.artist_id = artist_search_results['id']
        self.artist_popularity = artist_search_results['popularity']
        self.artist_genre = artist_search_results['genres']
        self.artist_genres = self.genres_to_value(self.artist_genre)
        try:
            self.artist_image = artist_search_results['images'][1]['url']
        except IndexError:
            self.artist_image = ''

    def search_related_artists(self):
        related_artists = spotify.artist_related_artists(self.artist_id)
        for artist in related_artists['artists']:
            related_artist_name = artist['name']
            related_artist_id = artist['id']
            related_artist_popularity = artist['popularity']
            related_artist_genre = artist['genres']
            try:
                related_artist_image = artist['images'][1]['url']
            except IndexError:
                related_artist_image = ''
            self.related_artist_names.append(related_artist_name)
            self.related_artist_ids.append(related_artist_id)
            self.related_artist_popularities.append(related_artist_popularity)
            self.related_artist_genres.append(self.genres_to_value(related_artist_genre))
            self.related_artist_images.append(related_artist_image)

    def genres_to_value(self, artist_genres):
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
            return sum(genre_values) / sum(count_genres.values())

    def plot_network(self):
        artists = [[(self.artist_name, related_artist_name) for related_artist_name in self.related_artist_names]]
        node_color = deepcopy(self.related_artist_genres)
        node_color.insert(0, self.artist_genres)

        [self.G.add_edges_from(artist) for artist in artists]
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(self.G)
        node_size = [60 * self.artist_popularity]
        for popularity in self.related_artist_popularities:
            node_size.append(60 * popularity)
        nodes = nx.draw_networkx_nodes(self.G, pos, node_color=node_color, cmap=node_cmap, node_size=node_size, vmin=0, vmax=self.max_value)
        nodes.set_edgecolor('#f5f5f5')
        nx.draw_networkx_labels(self.G, pos, font_size=7)
        nx.draw_networkx_edges(self.G, pos, alpha=0.5)
        plt.axis('off')
        sm = plt.cm.ScalarMappable(cmap=node_cmap)
        sm._A = []
        plt.colorbar(sm, ticks=[])
        plt.show()

    def json_write(self):
        artists_dict = {
            'source': {
                'name': self.artist_name,
                'genre': self.artist_genres,
                'id': self.artist_id,
                'image': self.artist_image
            },
            'related': {
                'names': self.related_artist_names,
                'genres': self.related_artist_genres,
                'ids': self.related_artist_ids,
                'images': self.related_artist_images
            }
        }
        node_link_data = nx.readwrite.json_graph.node_link_data(self.G, {'name': 'name', 'target': 'related'})
        with open(os.path.join(current_dir, 'data/genres.json'), 'w') as f:
            json.dump(self.genres, f, ensure_ascii=False, indent=2)
        with open(os.path.join(current_dir, 'data/artists.json'), 'w') as f:
            json.dump(artists_dict, f, ensure_ascii=False, indent=2)
        with open(os.path.join(current_dir, 'data/node_link_data.json'), 'w') as f:
            json.dump(node_link_data, f, ensure_ascii=False, indent=2)

    def main(self):
        if len(self.artist_id) != 0:
            self.search_artist_from_id()
        elif len(self.artist_name) != 0:
            self.search_artist_from_name()
        else:
            sys.exit('Input at least one letter')
        self.search_related_artists()
        self.plot_network()
        self.json_write()

if __name__ == "__main__":
    source_artist_name = 'Sheena Ringo'
    source_artist_id = ''   # Sheena Ringo's ID: 2XjqKvB2Xz9IdyjWPIHaXi
    if len(source_artist_id) != 0:
        an = ArtistsNetwork(artist_id=source_artist_id)
    else:
        an = ArtistsNetwork(artist_name=source_artist_name)
    an.main()
