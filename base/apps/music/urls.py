from django.urls import path
from .views import ArtistListView, ArtistDetailView, MusicListView, MusicDetailView

urlpatterns = [
    # Artist routes
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('artists/<int:artist_id>/', ArtistDetailView.as_view(), name='artist-detail'),

    # Music routes
    path('music/', MusicListView.as_view(), name='music-list'),
    path('music/<int:music_id>/', MusicDetailView.as_view(), name='music-detail'),
]
