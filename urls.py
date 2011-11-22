from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
  (r'^static/photos/?', 'homepage.views.secure'),
  (r'^static/cache/?', 'homepage.views.secure'),
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  (r'^admin/', include(admin.site.urls)),
  (r'^/?', include('homepage.urls'))
)
