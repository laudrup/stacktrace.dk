from django.urls import path
from homepage import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('post/<post_id>/', views.post),
    path('project/<project_id>/', views.project),
    path('comments/<post_id>/', views.comments),
    path('comment/<post_id>/', views.comment),
    path('photos/<gallery_id>/', views.photos),
    path('photos/', views.photos, name='photos'),
    path('', views.index, name='index')
]
