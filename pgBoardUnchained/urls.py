from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from pgBoardUnchained import settings 
from board import urls as board_urls
from avatar import urls as avatar_urls
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(avatar_urls)),
    url(r'^', include(board_urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
