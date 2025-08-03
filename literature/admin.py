from django.contrib import admin
from .models import Journal, Literature, LiteratureUser

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'impact_factor', 'cas_partition', 'jcr_partition')
    search_fields = ('name',)

@admin.register(Literature)
class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'journal', 'pub_year', 'pub_date', 'created_at')
    search_fields = ('title', 'authors')
    list_filter = ('journal', 'pub_year', 'pub_date', 'created_at')
    date_hierarchy = 'pub_date'

@admin.register(LiteratureUser)
class LiteratureUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'literature', 'rating', 'is_favorite', 'created_at')
    search_fields = ('user__username', 'literature__title')
    list_filter = ('rating', 'is_favorite', 'created_at')
