from django.db import models


class SongManager(models.Manager):
    def create_song(self, name, author):
        song = self.create(name=name, author=author)
        # do something with the book
        return song


class Song(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'shazam_song'
    #objects = SongManager(using='postgres')


class FingerprintManager(models.Manager):
    def create_fingerprint(self, hash_value, time_stamp, song_id):
        song = self.create(hash_value=hash_value, time_stamp=time_stamp, song_id=song_id)


class Fingerprint(models.Model):
    hash_value = models.CharField(max_length=200)
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    time_stamp = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'shazam_fingerprint'


