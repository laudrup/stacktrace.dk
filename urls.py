from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#urlpatterns = []

#if settings.DEBUG:
#    urlpatterns += patterns('',
#    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
#    )


admin.autodiscover()

#(r'^data/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.BASE_CONTENT_PATH})

urlpatterns = patterns('',
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  (r'^admin/', include(admin.site.urls)),
  (r'^/?', include('homepage.urls'))
)

#urlpatterns += staticfiles_urlpatterns()
