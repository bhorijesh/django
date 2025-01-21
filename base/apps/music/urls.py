from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', index.as_view(), name='index'),
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('artists/create/', artist_create.as_view(), name='artist-create'),
    path('artists/<int:artist_id>/', ArtistDetailView.as_view(), name='artist-detail'),
    path('music/', MusicListView.as_view(), name='music-list'),
    path('music/create/', music_create.as_view(), name='music-create'),
    path('music/<int:music_id>/', MusicDetailView.as_view(), name='music-detail'),
    path('delete/<int:pk>/', delete.as_view() , name = "delete"),
    # path('delete/<int:playlist_id>/', play_delete.as_view() , name = "delete_playlist"),
    path('update/<int:pk>', update.as_view() , name = "update"),
    path('register/', register.as_view() , name ='register'),
    path('logout/', logout_page , name ='logout_page' ),
    path('', login_user.as_view(), name='login'),
    path('search/', search, name='search'), 
    path('playlist/', PlaylistView.as_view(), name='playlist-list'),
    path('playlist/<int:user_id>/<int:music_id>/', playlist.as_view(), name='playlist_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
