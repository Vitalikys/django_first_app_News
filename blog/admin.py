from django.contrib import admin
from .models import News, Category
# user: admin       passw: admin

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','category', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',) # leave , it's tuple

admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

# Register your models here.
