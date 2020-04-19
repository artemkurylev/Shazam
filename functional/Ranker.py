from functional.Indexer import calculate_n_grams
from codegen import generate_code
import pickle
from Levenshtein import distance as levenshtein_distance
from fingerprint import create_fingerprint
if __name__ == '__main__':
    # code = generate_code('../echoprint-codegen','../RoddyRicchTheBox.mp3')
    #
    # k_grams = calculate_n_grams(code, 5)
    #
    # with open('../test_dir/n_grams.p','rb') as rf:
    #     index = pickle.load(rf)
    #
    # with open('../test_dir/track_artists.p', 'rb') as rf:
    #     artists = pickle.load(rf)
    # with open('../test_dir/track_features.p', 'rb') as rf:
    #     features = pickle.load(rf)
    # scores = {}
    # print(features['0nbXyq5TXYPCO7pr3N8S4I'])
    # for idx, track in enumerate(index):
    #     distance = levenshtein_distance(code, features[track]['track']['echoprintstring'])
    #     scores.update({track: distance})
    # result = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1])}
    # with open('../test_dir/track_names.p', 'rb') as rf:
    #     names = pickle.load(rf)
    #
    # for idx, x in enumerate(result):
    #     if idx > 10:
    #         break
    #     print(names[x])
    with open('../test_dir/track_peaks.p','rb') as rf:
        names_peaks = pickle.load(rf)

    for name in names_peaks:
        print(name)

    fingerprint = create_fingerprint('ib17_r6_Damilola (mp3cut.net) (2).mp3')
    scores = {}
    print(len(fingerprint))
    for name in names_peaks:
        intersect = names_peaks[name].intersection(fingerprint)
        scores.update({name: len(intersect)})
        # j = 0
        # while j < len(names_peaks[name]) - 1:
        #     k = 0
        #
        #     while k < len(fingerprint) - 1:
        #         try:
        #             if fingerprint[k][0] == names_peaks[name][j][0]:
        #                 scores[name] += 1
        #                 # x = k + 1
        #                 # y = j + 1
        #                 # try:
        #                 #     while x < len(fingerprint) - 1 and y < len(names_peaks[name]) - 1:
        #                 #         x += 1
        #                 #         y += 1
        #                 #         if fingerprint[x][0] == names_peaks[name][y][0]:
        #                 #             scores[name] += 1
        #                 #     j = y - 1
        #                 #     k = x
        #                 # except IndexError:
        #                 #     print(x, y)
        #         except IndexError:
        #             print('It is KKKK', k, len(fingerprint))
        #             print('It Is JJJJJ', j, len(names_peaks[name]))
        #         k += 1
        #     j += 1

    print(scores)
