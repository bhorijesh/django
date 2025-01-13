from django import forms
from .models import Artist, Music
from django.contrib.auth.models import User

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre']

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['title', 'artist', 'genre', 'release_date']

class authForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ['username', 'password']