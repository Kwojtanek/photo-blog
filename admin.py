__author__ = 'Qba'
from  django.contrib import admin
from models import Foto, Album

class FotoInline(admin.StackedInline):
    model = Foto
    extra = 0

class AdminAlbum(admin.ModelAdmin):
    inlines = [FotoInline]

class AdminFoto(admin.ModelAdmin):
    list_display = ["data", 'albumy', 'miniaturka', "ISO", 'ekspozycja', 'f']

admin.site.register(Album,AdminAlbum)
admin.site.register(Foto, AdminFoto)

