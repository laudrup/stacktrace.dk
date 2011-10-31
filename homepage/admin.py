from django.contrib import admin
from models import *

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added')
    list_filter = ['date_added']
    date_hierarchy = 'date_added'
    #prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('photos',)

admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Gallery, GalleryAdmin)
