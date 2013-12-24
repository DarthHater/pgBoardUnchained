from django.conf.urls import patterns, include, url

#I like splitting url patterns into logical chunks:

#accounts
urlpatterns = patterns("",
    url(r'^account/login/$', 'board.views.login'),
    url(r'^account/logout/$', 'board.views.logout')
    )

#threads
urlpatterns +=(
    url(r'^thread/view/(\d+)/$', 'board.views.thread'),
    url(r'^thread/reply/(?P<pk>\d+)/$', 'board.views.reply', name='reply'),
    url(r'^thread/new/', 'board.views.post', name='post'),
    url(r'^thread/post/', 'board.views.new_thread', name='new_thread'),
    url(r'^thread/view/(\d+)/$', 'board.views.post')
    )

#node-testing
urlpatterns +=(
    url(r'^test/(\d+)/$', 'board.views.test', name='test'),
    url(r'^thread_api$', 'board.views.thread_api', name='thread_api'),
    )

#boards
urlpatterns +=(
    url(r'', 'board.views.list'),
    url(r'^list/(\d+)/$', 'board.views.list', name='list_threads')
	)