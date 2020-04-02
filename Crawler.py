import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from librosa import load as librosa_load
import librosa
import matplotlib.pyplot as plt
import numpy as np
import math
import subprocess
import json
import os
import pickle


class Crawler:

    def __init__(self, path_to_creds):
        self.track_names = {}
        self.track_features = {}
        self.track_artists = {}
        try:
            with open(path_to_creds, 'r') as rf:
                creds = json.load(rf)
                try:
                    self.client_credentials_manager = SpotifyClientCredentials(client_id=creds['client_id'],
                                                                               client_secret=creds['client_secret'])
                    self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager,
                                                   auth_manager=self.client_credentials_manager)
                except KeyError:
                    print('Wrong format of JSON file, you need to include information about client id and secret key')
        except FileNotFoundError:
            print("File doesn't exist")

    def crawl(self, path_to_save):
        if not os.path.exists(path_to_save):
            os.mkdir(path_to_save)
        for i in range(10):
            print('iteration number:', i)
            track_results = self.spotify.search(q='year:1980-2020', limit=50, offset=i*50)
            for j, t in enumerate(track_results['tracks']['items']):
                self.track_features.update({t['id']: self.spotify.audio_analysis(t['id'])})
                self.track_names.update({t['id']: t['name']})
                self.track_artists.update({t['id']: t['artists']})

        with open(os.path.join(path_to_save, 'track_features.p'), 'wb') as fp:
            pickle.dump(self.track_features, fp)
        with open(os.path.join(path_to_save, 'track_names.p'), 'wb') as fp:
            pickle.dump(self.track_names, fp)
        with open(os.path.join(path_to_save, 'track_artists.p'), 'wb') as fp:
            pickle.dump(self.track_artists, fp)


if __name__ == '__main__':
    crawler = Crawler('credentials.json')
    crawler.crawl('test_dir')
