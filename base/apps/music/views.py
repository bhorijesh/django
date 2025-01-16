from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Artist, Music
from .serializers import ArtistSerializer, MusicSerializer
from .forms import ArtistForm, MusicForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from templates import music

# Artist List View (for listing all artists and creating a new artist)
class ArtistListView(APIView):
    def get(self, request):
        # Force the rendering of HTML for browsers (regardless of the Accept header)
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') or 'application/xhtml+xml' in request.META.get('HTTP_ACCEPT', ''):
            artists = Artist.objects.all()
            return render(request, 'music/artist_list.html', {'artists': artists})  # HTML response
        else:
            artists = Artist.objects.all()
            serializer = ArtistSerializer(artists, many=True)
            return Response(serializer.data)  # JSON response for API clients

    def post(self, request):
        # Create a new artist via API
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

        # Force HTML rendering for browser requests (with Accept header checking)
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') or 'application/xhtml+xml' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'music/artist_detail.html', {'artist': artist})  # HTML response for browser
        else:
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)  # JSON response for API clients

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
        # Force the rendering of HTML for browsers (regardless of Accept header)
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') or 'application/xhtml+xml' in request.META.get('HTTP_ACCEPT', ''):
            music = Music.objects.all()
            return render(request, 'music/music_list.html', {'music_list': music})  # HTML response for browser
        else:
            music = Music.objects.all()
            serializer = MusicSerializer(music, many=True)
            return Response(serializer.data)  # JSON response for API clients

    def post(self, request):
        # Create a new music record via API
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

        # Force HTML rendering for browser requests (with Accept header checking)
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') or 'application/xhtml+xml' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'music/music_detail.html', {'music': music})  # HTML response for browser
        else:
            serializer = MusicSerializer(music)
            return Response(serializer.data)  # JSON response for API clients

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

@login_required
def index(request):
    music = Music.objects.all()
    return render(request, 'music/index.html', {'music_list': music})

# Artist Creation View (for creating an artist through a form)
@login_required
def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artist-list')
    else:
        form = ArtistForm()
    return render(request, 'music/artist_form.html', {'form': form})


# Music Creation View (for creating a music record through a form)
@login_required
def music_create(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('music-list')
    else:
        form = MusicForm()
    return render(request, 'music/music_form.html', {'form': form}) 

def delete(request,music_id):
    music = Music.objects.get(id=music_id)
    music.delete()
    return redirect('index')    

def update(request, music_id):
    music = Music.objects.get(id=music_id)
    if request.method == 'POST':
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            form.save()
            return redirect('index')  
    else:
        form = MusicForm(instance=music)

    return render(request, 'music/update.html', {'form': form, 'music': music})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')  
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                return redirect('index')  
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form.add_error(None, 'Form is invalid')

    else:
        form = AuthenticationForm()

    return render(request, 'music/form.html', {'form': form})   

def logout_page(request):
    logout(request)
    return redirect ('login')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request , 'Username already taken')
            return redirect('register')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account successfully created')
        return redirect('login')
    return render(request, 'music/register.html')
    

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')