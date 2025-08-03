from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import Question, Answer, Tag, Vote, Collection
from .serializers import (
    QuestionSerializer, 
    AnswerSerializer, 
    TagSerializer,
    QuestionListSerializer
)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """根据动作类型设置不同的权限"""
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'upvote_count', 'view_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """根据动作类型返回对应的序列化器"""
        if self.action == 'list':
            return QuestionListSerializer
        return QuestionSerializer

    def get_queryset(self):
        """获取问题查询集，支持多种过滤条件"""
        queryset = super().get_queryset()
        
        # 标签过滤
        tags = self.request.query_params.getlist('tags')
        if tags and tags != ['']:  # 确保tags不为空且不是空字符串
            queryset = queryset.filter(tags__name__in=tags).distinct()
        
        # 我的收藏
        if self.request.query_params.get('collected'):
            content_type = ContentType.objects.get_for_model(Question)
            collected_ids = Collection.objects.filter(
                user=self.request.user,
                content_type=content_type
            ).values_list('object_id', flat=True)
            queryset = queryset.filter(id__in=collected_ids)
        
        # 我的问题
        if self.request.query_params.get('my'):
            queryset = queryset.filter(author=self.request.user)
        
        # 热门问题（基于浏览量和赞同数）
        if self.request.query_params.get('hot'):
            queryset = queryset.annotate(
                hot_score=Count('view_count') + Count('upvote_count')
            ).order_by('-hot_score')
        
        return queryset.select_related('author').prefetch_related('tags')

    def perform_create(self, serializer):
        """创建新问题"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """赞同问题"""
        question = self.get_object()
        content_type = ContentType.objects.get_for_model(Question)
        
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=question.id,
            defaults={'vote_type': 'up'}
        )
        
        if not created:
            if vote.vote_type == 'up':
                vote.delete()
                question.upvote_count = max(0, question.upvote_count - 1)
            else:
                vote.vote_type = 'up'
                vote.save()
                question.upvote_count += 1
                question.downvote_count = max(0, question.downvote_count - 1)
        else:
            question.upvote_count += 1
        
        question.save()
        return Response({'upvote_count': question.upvote_count})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        """反对问题"""
        question = self.get_object()
        content_type = ContentType.objects.get_for_model(Question)
        
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=question.id,
            defaults={'vote_type': 'down'}
        )
        
        if not created:
            if vote.vote_type == 'down':
                vote.delete()
                question.downvote_count = max(0, question.downvote_count - 1)
            else:
                vote.vote_type = 'down'
                vote.save()
                question.downvote_count += 1
                question.upvote_count = max(0, question.upvote_count - 1)
        else:
            question.downvote_count += 1
        
        question.save()
        return Response({'downvote_count': question.downvote_count})

    @action(detail=True, methods=['post'])
    def collect(self, request, pk=None):
        """收藏问题"""
        question = self.get_object()
        content_type = ContentType.objects.get_for_model(Question)
        
        collection, created = Collection.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=question.id
        )
        
        if not created:
            collection.delete()
            question.collect_count = max(0, question.collect_count - 1)
        else:
            question.collect_count += 1
        
        question.save()
        return Response({'collect_count': question.collect_count})

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """增加浏览量"""
        question = self.get_object()
        question.view_count += 1
        question.save()
        return Response({'view_count': question.view_count})

class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """根据动作类型设置不同的权限"""
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """获取回答查询集
        - 列表视图：返回特定问题下的回答
        - 详情视图：返回所有回答
        """
        if self.action == 'list':
            return Answer.objects.filter(question_id=self.kwargs['pk'])
        return Answer.objects.all()

    def perform_create(self, serializer):
        """创建新回答"""
        question = Question.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, question=question)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """接受为最佳答案"""
        answer = self.get_object()
        question = answer.question
        
        if question.author != request.user:
            return Response(
                {'error': '只有问题作者可以设置最佳答案'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 取消之前的最佳答案
        Answer.objects.filter(question=question).update(is_accepted=False)
        
        # 设置新的最佳答案
        answer.is_accepted = True
        answer.save()
        
        return Response({'is_accepted': True})

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """赞同回答"""
        answer = self.get_object()
        content_type = ContentType.objects.get_for_model(Answer)
        
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=answer.id,
            defaults={'vote_type': 'up'}
        )
        
        if not created:
            if vote.vote_type == 'up':
                vote.delete()
                answer.upvote_count = max(0, answer.upvote_count - 1)
            else:
                vote.vote_type = 'up'
                vote.save()
                answer.upvote_count += 1
                answer.downvote_count = max(0, answer.downvote_count - 1)
        else:
            answer.upvote_count += 1
        
        answer.save()
        return Response({'upvote_count': answer.upvote_count})

    @action(detail=True, methods=['post'])
    def downvote(self, request, question_pk=None, pk=None):
        """反对回答"""
        answer = self.get_object()
        content_type = ContentType.objects.get_for_model(Answer)
        
        vote, created = Vote.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=answer.id,
            defaults={'vote_type': 'down'}
        )
        
        if not created:
            if vote.vote_type == 'down':
                vote.delete()
                answer.downvote_count = max(0, answer.downvote_count - 1)
            else:
                vote.vote_type = 'down'
                vote.save()
                answer.downvote_count += 1
                answer.upvote_count = max(0, answer.upvote_count - 1)
        else:
            answer.downvote_count += 1
        
        answer.save()
        return Response({'downvote_count': answer.downvote_count})

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """获取热门标签"""
        popular_tags = Tag.objects.annotate(
            question_count=Count('question')
        ).order_by('-question_count')[:10]
        
        serializer = self.get_serializer(popular_tags, many=True)
        return Response(serializer.data)