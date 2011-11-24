from django.contrib import admin
from models import *

class PhotoInline(admin.StackedInline):
    model = Photo

class GalleryAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(GalleryUpload)
admin.site.register(Gallery, GalleryAdmin)
