from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True , blank=True)
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True, null=True)
    debut_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True , blank=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)  # For song duration
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    album = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Music, related_name='playlists', blank=True)

    def __str__(self):
        return self.name
