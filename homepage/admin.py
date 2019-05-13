from django.contrib import admin
from . import models

class PhotoInline(admin.StackedInline):
    model = models.Photo

class GalleryAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]

admin.site.register(models.Post)
admin.site.register(models.Project)
admin.site.register(models.Comment)
admin.site.register(models.GalleryUpload)
admin.site.register(models.Gallery, GalleryAdmin)
