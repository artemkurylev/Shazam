from django.shortcuts import render
import io
from pydub import AudioSegment
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from shazam.functional.fingerprint import create_fingerprint
import time
from shazam.models import Fingerprint
from shazam.models import Song
import soundfile as sf
import audioread


@csrf_protect
def index(request):
    template = loader.get_template('shazam/index.html')
    return HttpResponse(template.render(request=request))


@csrf_protect
def upload_audio(request):
    audio_file = request.FILES.get('audio_data').read()
    s = io.BytesIO(audio_file)
    sr = 44100
    data, sample_rate = sf.read(s)
    sf.write('2.wav', data, samplerate=44100)
    # audio = AudioSegment.from_raw(s, sample_width=2, frame_rate=44100, channels=1).export('2.mp3', format='mp3')
    fingerprint = create_fingerprint('2.wav', -1, {})
    all_matches = []

    scores = {}
    largest = 0
    largest_diff = 0
    song_id = -1

    for idx, one_hash in enumerate(fingerprint):
        print(idx, 'of', len(fingerprint))
        try:
            matches = Fingerprint.objects.using('postgres').filter(hash_value=one_hash)
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
    print(song_id)
    song = Song.objects.using('postgres').get(id=song_id)
    print(song.name)
    return HttpResponse("Found song:{}".format(song.name))


def upload_song(request):
    template = loader.get_template('shazam/upload_song.html')
    return HttpResponse(template.render())


@require_POST
@csrf_protect
def song_uploaded(request):
    result = request.FILES.get('music')
    song_name = request.POST.get('song_name')
    song_author = request.POST.get('author')
    if result.name.endswith('.wav'):
        audio_file = result.read()
        s = io.BytesIO(audio_file)
        sr = 44100
        data, sample_rate = sf.read(s)
        sf.write('2.wav', data, samplerate=44100)
        full_fingerprint = create_fingerprint('2.wav', -1, {})
        latest_song = Song.objects.last()

        song = Song.objects.create(id=latest_song.id + 1, name=song_name, author=song_author)
        print_id = Fingerprint.objects.last().id + 1
        for i in full_fingerprint:
            for j in range(len(full_fingerprint[i])):
                fingerprint = Fingerprint.objects.create(id=print_id, hash_value=i, song_id_id=song.id,
                                                         time_stamp=int(full_fingerprint[i][j][0]))
                print_id += 1
    return HttpResponse('Song uploadedd!')
