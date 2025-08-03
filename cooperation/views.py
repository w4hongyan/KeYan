from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg

from .models import CooperationPost, CooperationApplication, Skill, UserSkill
from .serializers import (
    CooperationPostSerializer,
    CooperationPostListSerializer,
    CooperationApplicationSerializer,
    SkillSerializer,
    UserSkillSerializer
)

class CooperationPostViewSet(viewsets.ModelViewSet):
    queryset = CooperationPost.objects.all()
    serializer_class = CooperationPostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cooperation_type', 'status', 'difficulty_level']
    search_fields = ['title', 'content', 'requirements']
    ordering_fields = ['created_at', 'budget', 'application_count', 'view_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """根据动作类型返回对应的序列化器"""
        if self.action == 'list':
            return CooperationPostListSerializer
        return CooperationPostSerializer

    def get_queryset(self):
        """获取合作帖子查询集，支持多种过滤条件"""
        queryset = super().get_queryset()
        
        # 技能过滤
        skills = self.request.query_params.getlist('skills')
        if skills:
            queryset = queryset.filter(required_skills__overlap=skills)
        
        # 预算范围
        min_budget = self.request.query_params.get('min_budget')
        max_budget = self.request.query_params.get('max_budget')
        if min_budget:
            queryset = queryset.filter(budget__gte=min_budget)
        if max_budget:
            queryset = queryset.filter(budget__lte=max_budget)
        
        # 我的发布
        if self.request.query_params.get('my_posts'):
            queryset = queryset.filter(publisher=self.request.user)
        
        # 我的申请
        if self.request.query_params.get('my_applications'):
            applied_post_ids = CooperationApplication.objects.filter(
                applicant=self.request.user
            ).values_list('post_id', flat=True)
            queryset = queryset.filter(id__in=applied_post_ids)
        
        # 推荐合作（基于用户技能匹配）
        if self.request.query_params.get('recommended'):
            user_skills = UserSkill.objects.filter(
                user=self.request.user
            ).values_list('skill__name', flat=True)
            if user_skills:
                queryset = queryset.filter(
                    required_skills__overlap=list(user_skills)
                ).exclude(publisher=self.request.user)
        
        return queryset.select_related('publisher').prefetch_related('applications')

    def perform_create(self, serializer):
        """创建新的合作帖子"""
        serializer.save(publisher=self.request.user)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """申请合作"""
        post = self.get_object()
        
        if post.publisher == request.user:
            return Response(
                {'error': '不能申请自己的合作'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if post.status != 'pending':
            return Response(
                {'error': '该合作已不接受申请'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CooperationApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                post=post,
                applicant=request.user
            )
            
            # 更新申请计数
            post.application_count = post.applications.filter(status='pending').count()
            post.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """查看申请列表"""
        post = self.get_object()
        
        # 只有发布者可以查看所有申请
        if request.user != post.publisher:
            return Response(
                {'error': '无权查看此合作的申请'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        applications = post.applications.select_related('applicant')
        serializer = CooperationApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """增加浏览量"""
        post = self.get_object()
        post.view_count += 1
        post.save()
        return Response({'view_count': post.view_count})

class CooperationApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = CooperationApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取特定合作帖子的申请列表"""
        return CooperationApplication.objects.filter(
            post_id=self.kwargs['post_pk']
        ).select_related('applicant', 'post')

    def perform_create(self, serializer):
        """创建新的合作申请"""
        post = CooperationPost.objects.get(pk=self.kwargs['post_pk'])
        serializer.save(applicant=self.request.user, post=post)

    @action(detail=True, methods=['post'])
    def review(self, request, post_pk=None, pk=None):
        """审核申请"""
        application = self.get_object()
        
        # 只有发布者可以审核
        if request.user != application.post.publisher:
            return Response(
                {'error': '无权审核此申请'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        action_type = request.data.get('action')
        review_note = request.data.get('review_note', '')
        
        if action_type not in ['accept', 'reject']:
            return Response(
                {'error': '无效的审核操作'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'accepted' if action_type == 'accept' else 'rejected'
        application.review_note = review_note
        application.reviewed_at = timezone.now()
        application.save()
        
        # 如果接受申请，更新合作状态
        if action_type == 'accept':
            application.post.status = 'in_progress'
            application.post.save()
        
        return Response({'status': application.status})

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category']

class UserSkillViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_skills(self, request):
        """获取我的技能"""
        skills = self.get_queryset().select_related('skill')
        serializer = self.get_serializer(skills, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """获取技能推荐"""
        user_skills = UserSkill.objects.filter(
            user=request.user
        ).values_list('skill__name', flat=True)
        
        # 基于用户已有技能推荐相关技能
        recommended_skills = Skill.objects.exclude(
            name__in=user_skills
        )[:10]
        
        serializer = SkillSerializer(recommended_skills, many=True)
        return Response(serializer.data)