import pickle
from fingerprint import create_fingerprint
if __name__ == '__main__':
    with open('../test_dir/track_peaks.p','rb') as rf:
        names_peaks = pickle.load(rf)

    fingerprint = create_fingerprint('noize.mp3')
    scores = {}
    largest = 0
    result_song =''
    for name in names_peaks:
        intersect = names_peaks[name].intersection(fingerprint)
        scores.update({name: len(intersect)})
        deltas = {}
        cur_largest = 0
        for con in intersect:
            time_delta = con[1]
            if time_delta in deltas:
                deltas[time_delta] += 1
            else:
                deltas.update({time_delta: 1})
            cur_largest = max(deltas[time_delta], cur_largest)
        if name == 'ib17_r6_Damilola.Karpow_c594a003b0.mp3':
            print(cur_largest)
        if cur_largest > largest:
            print(cur_largest)
            largest = cur_largest
            result_song = name
    print(result_song)

    print(sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:5])

