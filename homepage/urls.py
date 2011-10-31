from django.conf.urls.defaults import *

urlpatterns = patterns('homepage.views',
    (r'^about/', 'about'),
    (r'^contact/', 'contact'),
    (r'^post/(?P<post_id>\d+)/$', 'post'),
    (r'^project/(?P<project_id>\d+)/$', 'project'),
    (r'^comments/(?P<post_id>\d+)/$', 'comments'),
    (r'^comment/(?P<post_id>\d+)/$', 'comment'),
    (r'^photos/(?P<gallery_id>\S+)/$', 'photos'),
    (r'^photos/$', 'photos'),
    (r'^$', 'index')
)
