from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, FormView, CreateView, TemplateView,UpdateView,DeleteView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin



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
            paginator = Paginator(music, 6)  
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            return render(request, 'music/music_list.html', {'music_list': page_obj})
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

class index(LoginRequiredMixin, ListView):
    model = Music
    template_name = 'music/index.html'
    context_object_name = 'music_list'
    paginate_by = 6  # Show 6 items per page


    def get_queryset(self):
        return Music.objects.all() 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        music = Music.objects.all()
        paginator = Paginator(music, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['music_list'] = page_obj  # Pass paginated music list
        context['total_records'] = paginator.count  # Total music records
        context['total_pages'] = paginator.num_pages  # Total pages
        context['current_page'] = page_obj.number  # Current page
        context['has_previous'] = page_obj.has_previous()  # If previous page exists
        context['has_next'] = page_obj.has_next()  # If next page exists
        
        return context

# Artist Creation View (for creating an artist through a form)
class artist_create(LoginRequiredMixin,CreateView):
    model = Artist
    template_name = 'music/artist_form.html'
    form_class = ArtistForm
    success_url = reverse_lazy('artist-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class music_create(LoginRequiredMixin,CreateView):
    model = Music
    template_name = 'music/music_form.html'
    form_class = MusicForm
    success_url = reverse_lazy('music-list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class delete(DeleteView):
    model = Music
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        # Use the get_object() method to fetch the object to delete
        music = self.get_object()  
        music.delete()  # Perform the deletion
        return redirect(self.success_url)    

class play_delete(DeleteView):
    model =Playlist
    success_url = reverse_lazy('index')
    # Override to prevent rendering of a template
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Get the Music object
        self.object.delete()  # Delete the object
        return self.get_success_url()     

class update(UpdateView):
    model = Music
    form_class = MusicForm  # Fixed the typo here
    template_name = 'music/update.html'
    context_object_name = 'music'
    success_url = reverse_lazy('index')  # Use reverse_lazy for success_url

class login_user(LoginView):
    template_name = 'music/form.html'
    def form_invalid(self, form):
        # Optionally add a custom error message
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

def logout_page(request):
    logout(request)
    return redirect('login')

class register(FormView):
    template_name = 'music/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # Redirect to the login page after successful registration

    def form_valid(self, form):
        form.save()  # Save the new user
        messages.success(self.request, 'Account successfully created')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your registration')
        return super().form_invalid(form)


def search(request):
    query = request.GET.get('q', '')
    if query:
        # Perform search based on the query
        music_results = Music.objects.filter(title__icontains=query)
        artist_results = Artist.objects.filter(name__icontains=query)
    else:
        music_results = []
        artist_results = []

    return render(request, 'music/search.html', {
        'music_results': music_results,
        'artist_results': artist_results,
        'query': query,
    })

class PlaylistView(APIView):
    def get(self, request):
        # Check if the request is for a browser (HTML request)
        if 'text/html' in request.META.get('HTTP_ACCEPT', '') or 'application/xhtml+xml' in request.META.get('HTTP_ACCEPT', ''):
            # Get the user's playlists (assuming only "My Playlist" for simplicity)
            playlist = Playlist.objects.filter(user=request.user)  # Assuming each user has their own playlists
            return render(request, 'music/playlist_list.html', {'playlists': playlist})
        else:
            # For API clients, return playlist data as JSON
            playlists = Playlist.objects.filter(user=request.user)
            serializer = PlaylistSerializer(playlists, many=True)
            return Response(serializer.data)
# class playlist(ListView):
#     model = Playlist
#     template_name = 'musicl/playlist_list.html'
#     context_object_name ='playlist'

#     def get_queryset(self):
#         return Playlist.objects.filter(user=self.request.user)

class PlaylistCreateView(CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/playlist_create.html'  # Your template for creating the playlist
    context_object_name = 'form'
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user to the current logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the playlist list page after successfully creating the playlist
        return reverse_lazy('playlist-list')
    
class AddToPlaylistView(FormView):
    template_name = 'music/select_playlist.html'
    form_class = AddToPlaylistForm

    def dispatch(self, request, *args, **kwargs):
        # Get the music object from the URL and the user
        self.music = get_object_or_404(Music, id=self.kwargs['music_id'])
        self.user = get_object_or_404(User, id=self.kwargs['user_id'])  # Ensure you have the User model
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['music'] = self.music
        context['playlists'] = Playlist.objects.filter(user=self.user)
        return context

    def form_valid(self, form):
        # Get the selected playlist ID from the form
        playlist_id = form.cleaned_data['playlist_id']
        playlist = get_object_or_404(Playlist, id=playlist_id)

        # Add the music to the playlist
        playlist.music.add(self.music)

        # Redirect to a success page or playlist page
        return redirect('playlist_list')  # Update the redirect URL based on your needs

    def form_invalid(self, form):
        # Handle the case where the form is invalid
        return self.render_to_response(self.get_context_data(form=form))
