import sys
import time
import client_config
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from community import community_louvain
import collections
import itertools

client_id = client_config.client_id
client_secret = client_config.client_secret
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class ArtistsNetwork():
    def __init__(self, artist_name):
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
            self.artist_genres = artist_search_results['artists']['items'][artist_index]['genres']
        except IndexError:
            sys.exit('Input the correct artist name.')

    def search_related_artists(self):
        related_artists = spotify.artist_related_artists(self.artist_id)
        for artist in related_artists['artists']:
            name = artist['name']
            unique_id = artist['id']
            popularity = artist['popularity']
            genres = artist['genres']
            self.related_artist_names.append(name)
            self.related_artist_ids.append(unique_id)
            self.related_artist_popularities.append(popularity)
            self.related_artist_genres.append(genres)
    
    def gen_artists_list(self):
        self.artists = [[(self.artist_name, related_artist_name) for related_artist_name in self.related_artist_names]]

    def plot_network(self):
        G = nx.Graph()
        [G.add_edges_from(artist) for artist in self.artists]
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(G)
        node_size = [60 * self.artist_popularity]
        for popularity in self.related_artist_popularities:
            node_size.append(60 * popularity)
        nx.draw_networkx_nodes(G, pos, node_color='orange', node_size=node_size)
        nx.draw_networkx_labels(G, pos, font_size=7)
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        plt.axis('off')
        plt.show()
    
    def main(self):
        self.search_artist()
        self.search_related_artists()
        self.gen_artists_list()
        self.plot_network()

if __name__ == "__main__":
    # reference_artist_name = input('Artist Name: ')
    reference_artist_name = 'Sheena Ringo'
    aw = ArtistsNetwork(reference_artist_name)
    aw.main()
