from django.shortcuts import render
import io
from pydub import AudioSegment
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from shazam.functional.fingerprint import create_fingerprint
import time


def index(request):
    template = loader.get_template('shazam/index.html')
    return HttpResponse(template.render())


@csrf_protect
def upload_audio(request):
    audiofile = request.FILES.get('audio_data').read()
    s = io.BytesIO(audiofile)

    audio = AudioSegment.from_raw(s, sample_width=2, frame_rate=22050, channels=2).export('2.wav', format='wav')
    start_time = time.time()
    fingerprint = create_fingerprint('2.wav', -1, {})
    print(time.time() - start_time)
    print(fingerprint)
    return HttpResponse("Audio uploaded successful!")
