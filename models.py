# coding=utf-8
import os
from django.db import models
from thumbs import ImageWithThumbsField
from string import join
from settings import MEDIA_ROOT
from PIL.ExifTags import TAGS
from PIL import Image

# Create your models here.


class Album(models.Model):
    tytul = models.CharField(max_length=60, help_text='Obowiązkowy', verbose_name='Tytuł', null=False, blank=False)
    publikowany = models.BooleanField(default=True, help_text='Album jest widoczny dla wszystkich lub tylko administratora')

    class Meta:
        verbose_name_plural = 'Albumy'

    def __unicode__(self):
        return self.tytul

#noinspection PyUnresolvedReferences
class Foto(models.Model):
    zdjecie = ImageWithThumbsField(upload_to='media/', sizes=((410,410),(1920,1080)), verbose_name= "Zdjęcie")
    glowna = models.BooleanField(default=False, verbose_name="Zdjęcie jest tak śliczne, że opublikuję je na głównej stronie")
    albumy = models.ForeignKey(Album)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Foto'

    def __unicode__(self):
        return "Zdjecie nr: %s" % (int(self.pk))

    #Tworzy link do miniaturki ktora sie wyswietla w adminie

    def miniaturka(self):
        return """<a href="/media/%s"><img src="/media/%s.410x410.%s" /></a>""" % ((self.zdjecie.name, self.zdjecie.name[:-4],self.zdjecie.name[-3:]))
        #By nie omijac tagow html
    miniaturka.allow_tags = True

    def exif(self, meta):
        ret = {}
        img = Image.open(os.path.join(MEDIA_ROOT, self.zdjecie.name))
        try:
            info = img._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            return ret[meta]
        except:
            return "Brak danych"


    def ISO(self):
        return self.exif('ISOSpeedRatings')


    def ekspozycja(self):
        ekspozycja = self.exif('ExposureTime')

        if ekspozycja[0] >= ekspozycja[1]:
            return str(ekspozycja[0]/ekspozycja[1]) + ' sec'
        else:
            return str(ekspozycja[0]) + '/' + str(ekspozycja[1]) + ' sec'

    def f(self):
        f = self.exif('FNumber')
        #liczba f to stosunek ogniskowej do źrenicy wejściowej
        #W danych EXIF jest przechowywany jako tuple
        licznik = float(f[0])
        mianownik = float(f[1])
        if licznik and mianownik:
            return licznik/mianownik
        else:
            return "Brak danych"
