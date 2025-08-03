from rest_framework import generics, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Journal, Literature, LiteratureUser
from .serializers import JournalSerializer, LiteratureSerializer, LiteratureUserSerializer
from api.utils import ApiResponse

# Journal views
@extend_schema_view(
    get=extend_schema(
        operation_id='获取期刊列表',
        summary='获取期刊列表',
        description='获取所有期刊的列表信息'
    ),
    post=extend_schema(
        operation_id='创建期刊',
        summary='创建新期刊',
        description='创建一个新的期刊记录'
    )
)
class JournalListCreateView(generics.ListCreateAPIView):
    """
    期刊列表接口

    GET  /api/literature/journals/    获取期刊列表
    POST /api/literature/journals/    创建期刊
    """
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data, "获取期刊列表成功")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.created(serializer.data, "期刊创建成功")

@extend_schema_view(
    get=extend_schema(
        operation_id='获取期刊详情',
        summary='获取期刊详情',
        description='获取特定期刊的详细信息'
    ),
    put=extend_schema(
        operation_id='更新期刊',
        summary='更新期刊信息',
        description='更新期刊的完整信息'
    ),
    patch=extend_schema(
        operation_id='部分更新期刊',
        summary='部分更新期刊信息',
        description='部分更新期刊的字段信息'
    ),
    delete=extend_schema(
        operation_id='删除期刊',
        summary='删除期刊',
        description='删除指定的期刊记录'
    )
)
class JournalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    期刊详情接口

    GET    /api/literature/journals/{id}/    获取期刊详情
    PUT    /api/literature/journals/{id}/    更新期刊信息
    PATCH  /api/literature/journals/{id}/    部分更新期刊
    DELETE /api/literature/journals/{id}/    删除期刊
    """
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data, "获取期刊详情成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(serializer.data, "期刊更新成功")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(None, "期刊删除成功")

# Literature views
@extend_schema_view(
    get=extend_schema(
        operation_id='获取文献列表',
        summary='获取文献列表',
        description='获取所有文献的列表信息'
    ),
    post=extend_schema(
        operation_id='创建文献',
        summary='创建新文献',
        description='创建一个新的文献记录'
    )
)
class LiteratureListCreateView(generics.ListCreateAPIView):
    """
    文献列表接口

    GET    /api/literature/literatures/    获取文献列表
    POST   /api/literature/literatures/    创建文献
    """
    queryset = Literature.objects.all()
    serializer_class = LiteratureSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['journal', 'pub_year']
    search_fields = ['title', 'authors', 'keywords']
    ordering_fields = ['pub_year', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data, "获取文献列表成功")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.created(serializer.data, "文献创建成功")

@extend_schema_view(
    get=extend_schema(
        operation_id='获取文献详情',
        summary='获取文献详情',
        description='获取特定文献的详细信息'
    ),
    put=extend_schema(
        operation_id='更新文献',
        summary='更新文献信息',
        description='更新文献的完整信息'
    ),
    patch=extend_schema(
        operation_id='部分更新文献',
        summary='部分更新文献信息',
        description='部分更新文献的字段信息'
    ),
    delete=extend_schema(
        operation_id='删除文献',
        summary='删除文献',
        description='删除指定的文献记录'
    )
)
class LiteratureRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    文献详情接口

    GET    /api/literature/literatures/{id}/    获取文献详情
    PUT    /api/literature/literatures/{id}/    更新文献信息
    PATCH  /api/literature/literatures/{id}/    部分更新文献
    DELETE /api/literature/literatures/{id}/    删除文献
    """
    queryset = Literature.objects.all()
    serializer_class = LiteratureSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data, "获取文献详情成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(serializer.data, "文献更新成功")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(None, "文献删除成功")

# LiteratureUser views
@extend_schema_view(
    get=extend_schema(
        operation_id='获取用户文献列表',
        summary='获取用户文献列表',
        description='获取所有用户文献关联的列表信息'
    ),
    post=extend_schema(
        operation_id='创建用户文献关联',
        summary='创建用户文献关联',
        description='创建一个新的用户文献关联记录'
    )
)
class LiteratureUserListCreateView(generics.ListCreateAPIView):
    """
    用户文献关联列表接口

    GET    /api/literature/literature-users/    获取用户文献列表
    POST   /api/literature/literature-users/    创建用户文献关联
    """
    serializer_class = LiteratureUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['literature__journal', 'rating', 'is_favorite']
    search_fields = ['literature__title', 'literature__authors', 'notes']
    ordering_fields = ['created_at', 'updated_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        return LiteratureUser.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(serializer.data, "获取用户文献列表成功")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return ApiResponse.created(serializer.data, "用户文献关联创建成功")

@extend_schema_view(
    get=extend_schema(
        operation_id='获取用户文献详情',
        summary='获取用户文献详情',
        description='获取特定用户文献关联的详细信息'
    ),
    put=extend_schema(
        operation_id='更新用户文献关联',
        summary='更新用户文献关联',
        description='更新用户文献关联的完整信息'
    ),
    patch=extend_schema(
        operation_id='部分更新用户文献关联',
        summary='部分更新用户文献关联',
        description='部分更新用户文献关联的字段信息'
    ),
    delete=extend_schema(
        operation_id='删除用户文献关联',
        summary='删除用户文献关联',
        description='删除指定的用户文献关联记录'
    )
)
class LiteratureUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    用户文献关联详情接口

    GET    /api/literature/literature-users/{id}/    获取用户文献详情
    PUT    /api/literature/literature-users/{id}/    更新用户文献关联
    PATCH  /api/literature/literature-users/{id}/    部分更新用户文献
    DELETE /api/literature/literature-users/{id}/    删除用户文献关联
    """
    serializer_class = LiteratureUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LiteratureUser.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(serializer.data, "获取用户文献详情成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ApiResponse.success(serializer.data, "用户文献关联更新成功")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return ApiResponse.success(None, "用户文献关联删除成功")
from django.shortcuts import render

# Create your views here.
