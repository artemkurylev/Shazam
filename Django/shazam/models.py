from django.db import models


class Fingerprint(models.Model):
    hash_value = models.CharField(max_length=200)
    song_id = models.IntegerField()
    time_stamp = models.IntegerField()

