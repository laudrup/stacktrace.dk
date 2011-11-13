from django.conf.urls.defaults import *

urlpatterns = patterns('homepage.views',
    (r'^about/', 'about'),
    (r'^contact/', 'contact'),
    (r'^post/(?P<post_id>\d+)/$', 'post'),
    (r'^project/(?P<project_id>\d+)/$', 'project'),
    (r'^comments/(?P<post_id>\d+)/$', 'comments'),
    (r'^comment/(?P<post_id>\d+)/$', 'comment'),
    (r'^post/(?P<post_id>[\-\d\w]+)/$', 'post'),
    (r'^project/(?P<project_id>[\-\d\w]+)/$', 'project'),
    (r'^comments/(?P<post_id>[\-\d\w]+)/$', 'comments'),
    (r'^comment/(?P<post_id>[\-\d\w]+)/$', 'comment'),
    (r'^photos/(?P<gallery_id>\S+)/(?P<photo_id>\S+)$', 'photos'),
    (r'^photos/(?P<gallery_id>\S+)/$', 'photos'),
    (r'^photos/$', 'photos'),
    (r'^$', 'index')
)
