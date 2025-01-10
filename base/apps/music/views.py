from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Artist, Music
from .serializers import ArtistSerializer, MusicSerializer

# Artist List View (for listing all artists and creating a new artist)
class ArtistListView(APIView):
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new artist
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Artist Detail View (for retrieving, updating, or deleting a single artist)
class ArtistDetailView(APIView):
    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return Response({"detail": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return Response({"detail": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return Response({"detail": "Artist not found."}, status=status.HTTP_404_NOT_FOUND)
        
        artist.delete()
        return Response({"detail": "Artist deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Music List View (for listing all music records and creating a new music record)
class MusicListView(APIView):
    def get(self, request):
        music = Music.objects.all()
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new music record
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Music Detail View (for retrieving, updating, or deleting a single music record)
class MusicDetailView(APIView):
    def get(self, request, music_id):
        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({"detail": "Music not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MusicSerializer(music)
        return Response(serializer.data)

    def put(self, request, music_id):
        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({"detail": "Music not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, music_id):
        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({"detail": "Music not found."}, status=status.HTTP_404_NOT_FOUND)

        music.delete()
        return Response({"detail": "Music deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
