# Create your views here.
from django.shortcuts import render_to_response
from models import Foto, Album

def home(request):
    foto = Foto.objects.all()
    foto = foto.filter(glowna=True)
    albumy = Album.objects.all()
    albumy = albumy.filter(publikowany=True)
    return render_to_response('home.html', { "foto" : foto, "albumy" : albumy})


def album(request, pk):
    albumy = Album.objects.get(pk=pk)
    wszystkie_albumy = Album.objects.exclude(tytul = albumy.tytul)
    wszystkie_albumy = wszystkie_albumy.filter(publikowany=True)
    foto = albumy.foto_set.all()

    return render_to_response('album.html', { 'albumy' : albumy, 'foto' : foto, 'wszystkie_albumy' : wszystkie_albumy})
