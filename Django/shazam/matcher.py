from shazam.models import Fingerprint


def find_maximal_match(fingerprint):
    scores = {}
    largest = 0
    largest_diff = 0
    song_id = -1

    for idx, one_hash in enumerate(fingerprint):
        print(idx, 'of', len(fingerprint))
        try:
            matches = Fingerprint.objects.filter(hash_value=one_hash)
            for matched_fingerprint in matches:
                for x in fingerprint[one_hash]:
                    time_delta = matched_fingerprint.time_stamp - x[0]
                    if time_delta not in scores:
                        scores.update({time_delta: {}})
                    if matched_fingerprint.song_id not in scores[time_delta]:
                        scores[time_delta].update({matched_fingerprint.song_id: 0})
                    scores[time_delta][matched_fingerprint.song_id] += 1
                    if scores[time_delta][matched_fingerprint.song_id] > largest:
                        largest_diff = time_delta
                        largest = scores[time_delta][matched_fingerprint.song_id]
                        song_id = matched_fingerprint.song_id.id
                        print(matched_fingerprint.song_id.name)
        except Fingerprint.DoesNotExist:
            pass
    return song_id, largest
