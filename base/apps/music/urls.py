from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('artists/', ArtistListView.as_view(), name='artist-list'),
    path('artists/create/', artist_create, name='artist-create'),
    path('artists/<int:artist_id>/', ArtistDetailView.as_view(), name='artist-detail'),
    path('music/', MusicListView.as_view(), name='music-list'),
    path('music/create/', music_create, name='music-create'),
    path('music/<int:music_id>/', MusicDetailView.as_view(), name='music-detail'),
    path('delete/<int:music_id>/', delete , name = "delete"),
    path('update/<int:music_id>/', update , name = "update"),
    path('register/', register , name ='register'),
    path('logout/', logout_page , name ='logout_page' ),
    path('', login_user, name='login'),
    path('', search, name='search'), 
    path('about/', about, name='about'),  # Example about page
    path('contact/',contact, name='contact'),  
]
