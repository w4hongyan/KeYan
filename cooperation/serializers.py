from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CooperationPost, CooperationApplication, Skill, UserSkill

User = get_user_model()

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'created_at']

class UserSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_name', 'proficiency_level', 'verified']

class CooperationApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)
    applicant_avatar = serializers.SerializerMethodField()
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = CooperationApplication
        fields = [
            'id', 'post', 'post_title', 'applicant', 'applicant_name', 'applicant_avatar',
            'cover_letter', 'proposed_solution', 'proposed_price',
            'portfolio_url', 'relevant_experience', 'estimated_duration',
            'available_start_date', 'status', 'review_note', 'created_at',
            'reviewed_at'
        ]
        read_only_fields = ['applicant', 'created_at', 'reviewed_at', 'review_note']
    
    def get_applicant_avatar(self, obj):
        return None

class CooperationPostListSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source='publisher.username', read_only=True)
    publisher_avatar = serializers.SerializerMethodField()
    required_skills_display = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CooperationPost
        fields = [
            'id', 'title', 'cooperation_type', 'publisher_name', 'publisher_avatar',
            'budget', 'difficulty_level', 'status', 'created_at', 'deadline',
            'required_skills_display', 'application_count', 'tags'
        ]
    
    def get_publisher_avatar(self, obj):
        return None
    
    def get_required_skills_display(self, obj):
        return obj.required_skills
    
    def get_application_count(self, obj):
        return obj.applications.filter(status='pending').count()

class CooperationPostSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source='publisher.username', read_only=True)
    publisher_avatar = serializers.SerializerMethodField()
    applications = CooperationApplicationSerializer(many=True, read_only=True)
    required_skills_display = serializers.SerializerMethodField()
    
    class Meta:
        model = CooperationPost
        fields = [
            'id', 'title', 'content', 'cooperation_type', 'publisher', 'publisher_name',
            'publisher_avatar', 'requirements', 'reward_description', 'budget',
            'required_skills', 'required_skills_display', 'difficulty_level',
            'status', 'tags', 'deadline', 'expected_duration', 'view_count',
            'application_count', 'applications', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'publisher', 'created_at', 'updated_at', 'view_count',
            'application_count', 'applications'
        ]
    
    def get_publisher_avatar(self, obj):
        return None
    
    def get_required_skills_display(self, obj):
        skills = Skill.objects.filter(name__in=obj.required_skills)
        return SkillSerializer(skills, many=True).data

class CooperationPostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    required_skills = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    
    class Meta:
        model = CooperationPost
        fields = [
            'title', 'content', 'cooperation_type', 'requirements',
            'reward_description', 'budget', 'required_skills', 'difficulty_level',
            'tags', 'deadline', 'expected_duration'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        required_skills = validated_data.pop('required_skills', [])
        
        post = CooperationPost.objects.create(
            publisher=self.context['request'].user,
            required_skills=required_skills,
            **validated_data
        )
        
        post.tags = tags_data
        post.save()
        
        return post