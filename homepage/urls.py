from django.conf.urls.defaults import *

urlpatterns = patterns('homepage.views',
    (r'^about/', 'about'),
    (r'^contact/', 'contact'),
    (r'^post/(?P<post_id>\d+)/$', 'post'),
    (r'^$', 'index')
)
