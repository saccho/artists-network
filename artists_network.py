import sys
from copy import deepcopy
from conf import client
from conf.color_map import node_cmap
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import networkx as nx

client_id = client.client_id
client_secret = client.client_secret
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
spotify = Spotify(client_credentials_manager=client_credentials_manager)

class ArtistsNetwork():
    def __init__(self, artist_name):
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
        self.artist_name = artist_name
        self.related_artist_names = []
        self.related_artist_ids = []
        self.related_artist_popularities = []
        self.related_artist_genres = []
        
    def search_artist(self):
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
                        artist_search_result['popularity'], artist_search_result['images'][0]['url']))
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
        except IndexError:
            sys.exit('Input the correct artist name.')

    def search_related_artists(self):
        related_artists = spotify.artist_related_artists(self.artist_id)
        for artist in related_artists['artists']:
            related_artist_name = artist['name']
            related_artist_id = artist['id']
            related_artist_popularity = artist['popularity']
            related_artist_genre = artist['genres']
            self.related_artist_names.append(related_artist_name)
            self.related_artist_ids.append(related_artist_id)
            self.related_artist_popularities.append(related_artist_popularity)
            self.related_artist_genres.append(self.genres_to_value(related_artist_genre))

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

        G = nx.Graph()
        [G.add_edges_from(artist) for artist in artists]
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(G)
        node_size = [60 * self.artist_popularity]
        for popularity in self.related_artist_popularities:
            node_size.append(60 * popularity)
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_color, cmap=node_cmap, node_size=node_size, vmin=0, vmax=self.max_value)
        nodes.set_edgecolor('#f5f5f5')
        nx.draw_networkx_labels(G, pos, font_size=7)
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.axis('off')
        sm = plt.cm.ScalarMappable(cmap=node_cmap)
        sm._A = []
        plt.colorbar(sm, ticks=[])
        plt.show()
    
    def main(self):
        self.search_artist()
        self.search_related_artists()
        self.plot_network()

if __name__ == "__main__":
    reference_artist_name = input('Artist Name: ')
    an = ArtistsNetwork(reference_artist_name)
    an.main()
