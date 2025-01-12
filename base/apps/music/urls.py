from django.urls import path
from .views import ArtistListView, ArtistDetailView, MusicListView, MusicDetailView, artist_create, music_create, index,login_user

urlpatterns = [
    path('index/', index, name='index'),
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('artists/create/', artist_create, name='artist-create'),
    path('artists/<int:artist_id>/', ArtistDetailView.as_view(), name='artist-detail'),
    path('music/', MusicListView.as_view(), name='music-list'),
    path('music/create/', music_create, name='music-create'),
    path('music/<int:music_id>/', MusicDetailView.as_view(), name='music-detail'),
    path('', login_user, name='login')
]
