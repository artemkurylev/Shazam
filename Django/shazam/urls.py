from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'upload_audio/', views.upload_audio, name='upload_audio'),
    path(r'upload_song', views.upload_song, name='upload_song'),
    path(r'song_uploaded/', views.song_upload_wrapper, name='song_uploaded'),
    path(r'/song_uploaded/', views.song_upload_wrapper, name='song_uploaded')
]
