from django.conf.urls import url
from homepage import views

urlpatterns = [
    url(r'^about/?', views.about, name='about'),
    url(r'^contact/?', views.contact, name='contact'),
    url(r'^post/(?P<post_id>\d+)/?$', views.post),
    url(r'^project/(?P<project_id>\d+)/?$', views.project),
    url(r'^comments/(?P<post_id>\d+)/?$', views.comments),
    url(r'^comment/(?P<post_id>\d+)/?$', views.comment),
    url(r'^post/(?P<post_id>[\-\d\w]+)/?$', views.post),
    url(r'^project/(?P<project_id>[\-\d\w]+)/?$', views.project),
    url(r'^comments/(?P<post_id>[\-\d\w]+)/?$', views.comments),
    url(r'^comment/(?P<post_id>[\-\d\w]+)/?$', views.comment),
    url(r'^photos/(?P<gallery_id>\S+)/?$', views.photos),
    url(r'^photos/?$', views.photos, name='photos'),
    url(r'^$', views.index, name='index')
]
