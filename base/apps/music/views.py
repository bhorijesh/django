from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Artist, Music
from .serializers import ArtistSerializer, MusicSerializer


class ArtistListView(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)


class ArtistDetailView(APIView):
    def get(self, request, artist_id):
        artist = Artist.objects.get(id=artist_id)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


class MusicListView(APIView):
    def get(self, request):
        music = Music.objects.all()
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data)


class MusicDetailView(APIView):
    def get(self, request, music_id):
        music = Music.objects.get(id=music_id)
        serializer = MusicSerializer(music)
        return Response(serializer.data)
