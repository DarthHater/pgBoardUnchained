from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vivalavinyl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/login/$', 'board.views.login'),
    url(r'^account/logout/$', 'board.views.logout'),
    url(r'^thread/view/(\d+)/$', 'board.views.thread'),
    url(r'^thread/reply/(?P<pk>\d+)/$', 'board.views.reply', name='reply'),
    url(r'^thread/new/', 'board.views.post', name='post'),
    url(r'^thread/post/', 'board.views.new_thread', name='new_thread'),
    url(r'^thread/view/(\d+)/$', 'board.views.post'),
    url(r'', 'board.views.list'),
    url(r'^list/(\d+)/$', 'board.views.list', name='list_threads'),

)
