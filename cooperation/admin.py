from django.contrib import admin
from .models import CooperationPost, CooperationApplication, CooperationProgress, CooperationReview, Skill, UserSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'verified']
    list_filter = ['proficiency_level', 'verified']
    search_fields = ['user__username', 'skill__name']
    raw_id_fields = ['user', 'skill']

@admin.register(CooperationPost)
class CooperationPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'publisher', 'cooperation_type', 'status', 
        'budget', 'difficulty_level', 'application_count', 'created_at'
    ]
    list_filter = [
        'cooperation_type', 'status', 'difficulty_level', 
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'content', 'requirements']
    raw_id_fields = ['publisher']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(CooperationApplication)
class CooperationApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'post', 'applicant', 'status', 'proposed_price', 
        'estimated_duration', 'available_start_date', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = [
        'post__title', 'applicant__username', 'cover_letter'
    ]
    raw_id_fields = ['post', 'applicant']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

@admin.register(CooperationProgress)
class CooperationProgressAdmin(admin.ModelAdmin):
    list_display = ['cooperation', 'progress_percentage', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['cooperation__title', 'description']
    raw_id_fields = ['cooperation']
    date_hierarchy = 'created_at'

@admin.register(CooperationReview)
class CooperationReviewAdmin(admin.ModelAdmin):
    list_display = ['cooperation', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = [
        'cooperation__post__title', 'reviewer__username', 'content'
    ]
    raw_id_fields = ['cooperation', 'reviewer']
    date_hierarchy = 'created_at'