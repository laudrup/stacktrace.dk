from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
  (r'^admin/', include(admin.site.urls)),
  (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
  (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
  (r'^/?', include('homepage.urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
else:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'homepage.views.media'),
)
