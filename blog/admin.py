from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category
# user: admin       passw: admin

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','category', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    # fields to show in admin add form:
    fields = ('title','category', 'content', 'photo', 'get_photo',  'is_published', 'created_at', 'updated_at', 'views')
    readonly_fields = ('get_photo',  'created_at', 'updated_at', 'views')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src ="{obj.photo.url}" width="35">')
    save_on_top = True

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',) # leave , it's tuple

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

# Register your models here.
