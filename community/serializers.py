from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Question, Answer, Tag, Vote, Collection

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = Answer
        fields = [
            'id', 'content', 'author', 'author_name', 'author_avatar',
            'created_at', 'updated_at', 'upvote_count', 'downvote_count',
            'is_accepted'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_author_avatar(self, obj):
        # 这里可以返回用户头像URL
        return None

class QuestionListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    answer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'author_name', 'author_avatar', 'tags', 'created_at',
            'view_count', 'upvote_count', 'downvote_count', 'collect_count',
            'answer_count'
        ]
    
    def get_author_avatar(self, obj):
        # 这里可以返回用户头像URL
        return None
    
    def get_answer_count(self, obj):
        return obj.answers.count()

class QuestionSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    is_collected = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'title', 'content', 'author', 'author_name', 'author_avatar',
            'tags', 'created_at', 'updated_at', 'view_count',
            'upvote_count', 'downvote_count', 'collect_count',
            'answers', 'is_collected', 'user_vote'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_author_avatar(self, obj):
        # 这里可以返回用户头像URL
        return None
    
    def get_is_collected(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Question)
            return Collection.objects.filter(
                user=user,
                content_type=content_type,
                object_id=obj.id
            ).exists()
        return False
    
    def get_user_vote(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            content_type = ContentType.objects.get_for_model(Question)
            vote = Vote.objects.filter(
                user=user,
                content_type=content_type,
                object_id=obj.id
            ).first()
            return vote.vote_type if vote else None
        return None

class QuestionCreateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        question = Question.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        
        # 处理标签
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            question.tags.add(tag)
        
        return question

class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['content']