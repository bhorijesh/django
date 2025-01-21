from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1' ]