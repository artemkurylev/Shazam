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


class Crawler:
    def __init__(self, path_to_creds):
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

    def crawl(self):
        pass
        # ToDo


if __name__ == '__main__':
    crawler = Crawler('credentials.json')
