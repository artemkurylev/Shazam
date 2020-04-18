import os
import pickle


def calculate_n_grams(code, n):
    result = []
    for i in range(len(code) - n):
        result.append(code[i:i+n])
    return result


class Indexer:

    def __init__(self, path):
        self.path = path

    def index_tracks(self, n):
        try:
            with open(os.path.join(self.path, 'track_features.p'), 'rb') as rf:
                features = pickle.load(rf)
                rf.close()
        except FileNotFoundError:
            print('Error: could not find file, Index will not do anything')
            return False
        result = {}
        for track in features:
            n_grams = calculate_n_grams(features[track]['track']['echoprintstring'], n)
            result.update({track: n_grams})
        with open(os.path.join(self.path, 'n_grams.p'), 'wb') as wf:
            pickle.dump(result, wf)


if __name__ == '__main__':
    indexer = Indexer('../test_dir')
    indexer.index_tracks(2)





