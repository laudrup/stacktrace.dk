from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from homepage import views as homepage_views
from django.conf import settings

admin.autodiscover()

urlpatterns = [
  url(r'^admin/?', admin.site.urls),
  url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  url(r'^logout/?$', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
  url(r'^', include('homepage.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', homepage_views.media),
]
