from django.contrib import admin
from .models import Artist, Music


# Register your models here.
class MusicInline(admin.TabularInline):  
    model = Music
    extra = 1

class ArtistAdmin(admin.ModelAdmin):
    inlines = [MusicInline]
    list_display = ('name', 'genre', 'debut_date')
    search_fields = ('name', 'genre')

class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'album', 'genre')
    search_fields = ('title', 'artist__name')

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Music, MusicAdmin)
