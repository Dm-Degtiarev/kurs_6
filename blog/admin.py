from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class UserAdmin(admin.ModelAdmin):
    list_display = ('heading', 'content', 'image', 'views_count', 'publicate_date')
    search_fields = ('heading', 'content')
    list_filter = ('publicate_date',)
    list_display_links = ('heading',)
