from django.urls import include, re_path, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from homepage import views as homepage_views
from django.conf import settings

admin.autodiscover()

urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path('media/(?P<path>.*)$', homepage_views.media)
    ]
