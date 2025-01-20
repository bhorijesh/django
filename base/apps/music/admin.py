from django.contrib import admin
from .models import *


# Register your models here.
class MusicInline(admin.TabularInline):  
    model = Music
    extra = 1

class ArtistAdmin(admin.ModelAdmin):
    inlines = [MusicInline]
    list_display = ('name', 'genre', 'debut_date','image')
    search_fields = ('name', 'genre')

class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'album', 'genre','audio')
    search_fields = ('title', 'artist__name')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')  
    search_fields = ('name',)

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Music, MusicAdmin)
