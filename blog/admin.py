from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'cover', 'publish', 'status']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['commenter','post', 'body','created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['commenter', 'body']


admin.site.register(Like)
