from django.contrib import admin
from .models import Post, Comments, Likes

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'cover', 'publish', 'status']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Comments)
admin.site.register(Likes)
