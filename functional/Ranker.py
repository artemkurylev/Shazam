import pickle
from fingerprint import create_fingerprint
import time

if __name__ == '__main__':
    with open('../test_dir/index.p', 'rb') as rf:
        index = pickle.load(rf)
    with open('../test_dir/track_ids.p', 'rb') as rf:
        track_ids = pickle.load(rf)
    start_time = time.time()
    fingerprint = create_fingerprint('noize.mp3', -1, {})
    print('Fingerprint creating time: ', time.time() - start_time)
    scores = {}
    largest = 0
    largest_diff = 0
    song_id = -1

    for hash_code in fingerprint:
        if hash_code in index:
            for i in index[hash_code]:
                for x in fingerprint[hash_code]:
                    delta = i[0] - x[0]
                    if delta not in scores:
                        scores.update({delta: {}})
                    if i[1] not in scores[delta]:
                        scores[delta].update({i[1]: 0})
                    scores[delta][i[1]] += 1
                    if scores[delta][i[1]] > largest:
                        largest_diff = delta
                        largest = scores[delta][i[1]]
                        song_id = i[1]
    print('Time of the search(with creating of fingerprint)', time.time() - start_time)
    print(track_ids[song_id])
    print('Score: ', largest)

    # for name in names_peaks:
    #     intersect = names_peaks[name].intersection(fingerprint)
    #     scores.update({name: len(intersect)})
    #     deltas = {}
    #     cur_largest = 0
    #     for con in intersect:
    #         time_delta += con[1]
    #         if time_delta in deltas:
    #             deltas[time_delta] += 1
    #         else:
    #             deltas.update({time_delta: 1})
    #         cur_largest = max(deltas[time_delta], cur_largest)
    #     if name == 'ib17_r6_Damilola.Karpow_c594a003b0.mp3':
    #         print(cur_largest)
    #     if cur_largest > largest:
    #         print(cur_largest)
    #         largest = cur_largest
    #         result_song = name
    # print(result_song)
    #
    # print(sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:5])
