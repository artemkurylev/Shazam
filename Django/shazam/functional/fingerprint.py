import librosa
import os

from scipy import ndimage
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import hashlib
import pickle
import time

from hashlib import md5


def create_fingerprint(audio_path, id, index):
    audio, sr = librosa.load(audio_path, 22050)
    neighborhood_size = 40
    S = librosa.feature.melspectrogram(audio, sr=sr, n_mels=256, fmax=4000)
    S = librosa.power_to_db(S, ref=np.max)
    # get local maxima
    Sb = maximum_filter(S, neighborhood_size) == S

    Sbd, num_objects = ndimage.label(Sb)
    objs = ndimage.find_objects(Sbd)
    points = []
    for dy, dx in objs:
        x_center = (dx.start + dx.stop - 1) // 2
        y_center = (dy.start + dy.stop - 1) // 2
        if (dx.stop - dx.start) * (dy.stop - dy.start) == 1:
            points.append((x_center, y_center))
    points = sorted(points)
    pair_num = 20
    for i in range(len(points)):
        for j in range(1, pair_num):
            if i + j >= len(points):
                break

            freq1 = points[i][1]
            freq2 = points[i + j][1]
            t1 = points[i][0]
            t2 = points[i+j][0]
            t_delta = t2 - t1
            if 50 <= t_delta < 100 and abs(freq1 - freq2) < 100:
                string = str(str(freq1)+'|'+str(freq2) + '|'+str(t_delta))
                x = hashlib.sha1(string.encode())
                if x.hexdigest() in index:
                    index[x.hexdigest()].append((t1, id))
                else:
                    index.update({x.hexdigest(): [(t1, id)]})

    return index

if __name__ == '__main__':
    index = {}
    id_names = {}
    for idx, i in enumerate(os.listdir('audio_database/')):
        index = create_fingerprint(os.path.join('audio_database', i), idx, index)
        id_names.update({idx: i})
    with open('test_dir/index.p', 'wb') as wf:
        pickle.dump(index, wf)

    with open('test_dir/track_ids.p', 'wb') as wf:
        pickle.dump(id_names, wf)
