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

    def ISO(self):
        ret = {}
        i = Image.open(os.path.join(MEDIA_ROOT, self.zdjecie.name))
        try:
            info = i._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            return ret['ISOSpeedRatings']
        except:
            return "Brak danych"

    def ekspozycja(self):
        ret = {}
        i = Image.open(os.path.join(MEDIA_ROOT, self.zdjecie.name))
        try:
            info = i._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            if ret['ExposureTime'][0] >= ret['ExposureTime'][1]:
                return str(ret['ExposureTime'][0]/ret['ExposureTime'][1]) + ' sec'
            else:
                return str(ret['ExposureTime'][0]) + '/' + str(ret['ExposureTime'][1]) + ' sec'
        except:
            return "Brak Danych"
    def f(self):
        ret = {}
        i = Image.open(os.path.join(MEDIA_ROOT, self.zdjecie.name))
        try:
            info = i._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            return 'F ' + str(float(ret['FNumber'][0])/float(ret['FNumber'][1]))
        except:
            return "Brak Danych"