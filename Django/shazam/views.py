from django.shortcuts import render
import io
# Create your views here.
from django.http import HttpResponse,StreamingHttpResponse
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from shazam.functional.fingerprint import create_fingerprint
from shazam.matcher import find_maximal_match
from shazam.models import Fingerprint
from shazam.models import Song
import soundfile as sf
import pydub


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
    fingerprint, _ = create_fingerprint('2.wav', -1, {})
    all_matches = []
    print(len(fingerprint))
    song_id, largest_count = find_maximal_match(fingerprint)
    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return HttpResponse("Song unfortunately wasn't found, but be sure it will be added shortly!!!")

    print(song.name)
    return HttpResponse('Found song:{}  {}'.format(song.name, song.author))


def upload_song(request):
    template = loader.get_template('shazam/upload_song.html')
    return HttpResponse(template.render())


@require_POST
@csrf_protect
def song_upload_wrapper(request):
    print('Request first came to wrapper, now it is going further')
    return StreamingHttpResponse(song_uploaded(request))


@require_POST
@csrf_protect
def song_uploaded(request):
    result = request.FILES.get('music')
    song_name = request.POST.get('song_name')
    song_author = request.POST.get('author')
    print('We are in the right place')
    try:
        if result.name.endswith('.wav'):
            audio_file = result.read()
            s = io.BytesIO(audio_file)
            sr = 44100
            data, sample_rate = sf.read(s)
            sf.write('2.wav', data, samplerate=44100)
            full_fingerprint, hash_num = create_fingerprint('2.wav', -1, {})
        elif result.name.endswith('.mp3'):
            audio_file = result.read()
            with open('x.mp3', 'wb') as mp:
                mp.write(audio_file)
                mp.close()
            full_fingerprint, hash_num = create_fingerprint('x.mp3', -1, {})
            print('At least fingerprint was created:', len(full_fingerprint))

        latest_song = Song.objects.last()
        new_song_id = latest_song.id + 1
        print('It is ok here!!, we got the last song')
        print_id = Fingerprint.objects.last().id + 1
        fingerprints = []
        print('It is ok here, we got the last fingerprint')
        for i in full_fingerprint:
            for j in range(len(full_fingerprint[i])):
                fingerprints.append(Fingerprint(id=print_id, hash_value=i, song_id_id=new_song_id,
                                                time_stamp=int(full_fingerprint[i][j][0])))
                print_id += 1

        print(len(fingerprints))
        print('Before first yield everything is ok!!!')
        yield 'Song uploaded, now checking for matches in our database..'

        song_id, count = find_maximal_match(full_fingerprint)
        if count <= hash_num / 10:
            song = Song.objects.create(id=new_song_id, name=song_name, author=song_author)
            for fingerprint in fingerprints:
                fingerprint.save()
            yield'Song successfully saved in database'
        else:
            name = Song.objects.get(id=song_id).name
            yield '<p>It seems, that this song is actually duplicate of this song: ' + name + '</p>'
    except Exception as err:
        print(err)
        yield 'Something went wrong:' + str(err)
