from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

urlpatterns = []

urlpatterns = patterns('',
  (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
  (r'^admin/', include(admin.site.urls)),
  (r'^/?', include('homepage.urls'))
)
