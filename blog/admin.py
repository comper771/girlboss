from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'updated_at')


admin.site.register(Article, ArticleAdmin)
