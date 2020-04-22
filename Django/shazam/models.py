from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)


class Fingerprint(models.Model):
    hash_value = models.CharField(max_length=200)
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()


