from django import forms
from .models import *
from django.contrib.auth.models import User

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre','debut_date','bio','image']

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'genre', 'release_date','audio']

class authForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ['username', 'password']

class PlaylistForm(forms.ModelForm):
    music = forms.ModelMultipleChoiceField(queryset=Music.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Playlist
        fields = ['user', 'name', 'music']