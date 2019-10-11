from django.conf.urls import patterns, include, url
from django.contrib import admin
import home.views
from HomeCloud.settings import DEBUG, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'home.views.home', name='Home' ),
    url(r'^movie/(?P<movie_id>\d+)/$', 'home.views.movie_details', name='Movie'),
    url(r'^actor/(?P<actor_id>\d+)/$', 'home.views.actor_details', name='Actor'),

    url(r'^reload-database/$', 'home.file_importer.process_import_file', name='ReloadDatabase'),

    url(r'^accounts/login/$', 'home.views.view_login', name='Login'),
    url(r'^accounts/logout/$', 'home.views.view_logout', name='Logout'),
    url(r'^accounts/list/viewed/$', 'home.views.list_viewed', name='ViewedList'),
    url(r'^accounts/list/pending/$', 'home.views.list_pending', name='PendingList'),

    url(r'^search/$', 'home.views.search', name='Search'),
    url(r'^login-auth-q3qdas2/$', 'home.views.auto_login', name='AutoLogin'),

    url(r'^movie/remove_list/(?P<movie_id>\d+)/$', 'home.views.remove_list', name='RemoveList'),
    url(r'^movie/add_seen/(?P<movie_id>\d+)/$', 'home.views.add_to_seen_list', name='AddToSeen'),
    url(r'^movie/add_view/(?P<movie_id>\d+)/$', 'home.views.add_to_view_list', name='AddToView'),

    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': MEDIA_ROOT}),
    )