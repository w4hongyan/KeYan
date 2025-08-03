from django.contrib import admin
from .models import Tag, Question, Answer, Vote, Collection

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    list_filter = ['color', 'created_at']
    search_fields = ['name']
    ordering = ['-created_at']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'view_count', 'upvote_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'is_accepted', 'upvote_count', 'created_at']
    list_filter = ['is_accepted', 'created_at']
    search_fields = ['content']
    raw_id_fields = ['question', 'author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    date_hierarchy = 'created_at'