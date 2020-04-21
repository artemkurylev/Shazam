import librosa
import os
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,
                                      iterate_structure, binary_erosion)
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import hashlib
import pickle

from hashlib import md5


def create_fingerprint(audio_path, id, index):
    audio, sr = librosa.load(audio_path, 22050)
    stft = np.log10(np.abs(librosa.stft(y=audio, n_fft=1024))) * 10
    stft[stft == -np.inf] = 0
    print(stft.shape)
    array = np.transpose(stft)
    print(librosa.get_duration(audio) * 1000 / len(array))
    peaks = []
    window_size = 10
    for i in range(0, len(array), window_size * 2):
        lb = max(0, i-window_size)
        rb = min(i + window_size, len(array))
        frame_peaks = []
        for j in range(0, len(array[i]), window_size * 2):
            bb = max(j - window_size, 0)
            ub = min(j + window_size, len(array[i]))

            block = array[lb:rb, bb:ub]

            result = np.where(block == np.amax(block))

            max_i = result[0][0]
            max_j = result[1][0]
            max_i -= window_size
            max_j -= window_size
            if array[i+max_i][j + max_j] > 0.05:
                frame_peaks.append([j + max_j, i+max_i])
        peaks.extend(frame_peaks)

    pair_num = 20
    peaks = sorted(peaks, key=lambda s: s[1])
    for i in range(len(peaks)):
        for j in range(1, pair_num):
            if i + j >= len(peaks):
                break

            freq1 = peaks[i][0]
            freq2 = peaks[i + j][0]
            t1 = peaks[i][1]
            t2 = peaks[i+j][1]
            t_delta = t2 - t1
            if 0 <= t_delta < 200:
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
