from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'upload_audio/', views.upload_audio, name='upload_audio')
]