__author__ = 'Qba'
from django.conf.urls import patterns, url, include
from views import home, album
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home,  name='home'),
    url(r'^(\d+)/$', album ,name='album'),
)
