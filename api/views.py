from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from .serializers import UserRegistrationSerializer, UserDetailSerializer, UserProfileSerializer, BillingInfoSerializer
from .models import User, UserProfile, BillingInfo
from .utils import ApiResponse

@extend_schema(
    summary="用户注册",
    description="创建新的用户账户",
    operation_id="用户注册"
)
class UserRegistrationView(generics.CreateAPIView):
    """
    用户注册接口
    
    POST /api/register/    创建用户账户
    
    必填：username、password、email、nickname
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        处理用户注册请求

        处理流程：
        1. 验证输入数据的完整性和格式
        2. 检查用户名和邮箱是否已存在
        3. 创建新用户账户
        4. 返回新创建用户的详细信息（不包含密码）

        成功响应：
        - 状态码：201 Created
        - 返回：新创建用户的详细信息（不包含密码字段）

        错误响应：
        - 状态码：400 Bad Request
        - 返回：详细的错误信息，指出具体哪个字段验证失败
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # 处理验证错误，返回友好的错误提示
            return ApiResponse.validation_error(serializer.errors, "注册失败，请检查输入信息")
        user = serializer.save()
        user_data = UserDetailSerializer(user).data
        return ApiResponse.created(user_data, "用户注册成功")


@extend_schema(
    summary="用户登录",
    description="用户登录获取JWT令牌",
    operation_id="用户登录"
)
class UserLoginView(TokenObtainPairView):
    """
    用户登录接口
    
    POST /api/login/    用户登录获取访问令牌
    
    必填：username、password
    返回：access、refresh令牌
    """
    permission_classes = [AllowAny]


@extend_schema(
    summary="刷新令牌",
    description="使用刷新令牌获取新的访问令牌",
    operation_id="刷新令牌"
)
class UserRefreshTokenView(TokenRefreshView):
    """
    刷新令牌接口
    
    POST /api/token/refresh/    刷新访问令牌
    
    必填：refresh令牌
    返回：新的access令牌
    """
    permission_classes = [AllowAny]


@extend_schema(
    summary="用户详情",
    description="获取当前登录用户的详细信息",
    operation_id="用户详情"
)
class UserProfileView(APIView):
    """
    用户详情接口
    
    GET /api/profile/    获取当前用户信息
    
    需要身份验证
    返回：用户详细信息（包含积分、VIP等级等）
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        """
        获取当前用户信息

        成功响应：
        - 状态码：200 OK
        - 返回：用户详细信息
        """
        serializer = self.serializer_class(request.user)
        return ApiResponse.success(serializer.data, "获取用户信息成功")

    def put(self, request):
        """
        更新当前用户信息

        可更新字段：nickname、email、phone
        """
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data, "用户信息更新成功")
        return ApiResponse.validation_error(serializer.errors, "更新失败")


@extend_schema(
    summary="用户个人资料",
    description="获取和更新用户个人详细资料",
    operation_id="用户个人资料"
)
class UserProfileDetailView(APIView):
    """
    用户个人资料接口

    GET /api/profile/detail/    获取用户个人资料
    PUT /api/profile/detail/      更新用户个人资料
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        """获取用户个人资料"""
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        serializer = self.serializer_class(profile)
        return ApiResponse.success(serializer.data, "获取个人资料成功")

    def put(self, request):
        """更新用户个人资料"""
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data, "个人资料更新成功")
        return ApiResponse.validation_error(serializer.errors, "更新失败")


@extend_schema(
    summary="用户头像上传",
    description="上传用户头像",
    operation_id="用户头像上传"
)
class UserAvatarUploadView(APIView):
    """
    用户头像上传接口

    POST /api/profile/avatar/    上传用户头像
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """上传用户头像"""
        if 'avatar' not in request.FILES:
            return ApiResponse.error("请上传头像文件")
        
        user = request.user
        user.avatar = request.FILES['avatar']
        user.save()
        
        serializer = UserDetailSerializer(user)
        return ApiResponse.success(serializer.data, "头像上传成功")


@extend_schema(
    summary="账单信息管理",
    description="获取和管理用户的账单信息",
    operation_id="账单信息管理"
)
class BillingInfoView(APIView):
    """
    账单信息管理接口

    GET /api/profile/billing/     获取账单信息列表
    POST /api/profile/billing/    创建账单信息
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BillingInfoSerializer

    def get(self, request):
        """获取用户账单信息列表"""
        billing_infos = BillingInfo.objects.filter(user=request.user)
        serializer = self.serializer_class(billing_infos, many=True)
        return ApiResponse.success(serializer.data, "获取账单信息成功")

    def post(self, request):
        """创建新的账单信息"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return ApiResponse.created(serializer.data, "账单信息创建成功")
        return ApiResponse.validation_error(serializer.errors, "创建失败")


@extend_schema(
    summary="单条账单信息管理",
    description="更新和删除单条账单信息",
    operation_id="单条账单信息管理"
)
class BillingInfoDetailView(APIView):
    """
    单条账单信息管理接口

    PUT /api/profile/billing/{id}/    更新账单信息
    DELETE /api/profile/billing/{id}/ 删除账单信息
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BillingInfoSerializer

    def put(self, request, pk):
        """更新账单信息"""
        try:
            billing_info = BillingInfo.objects.get(pk=pk, user=request.user)
        except BillingInfo.DoesNotExist:
            return ApiResponse.error("账单信息不存在")
        
        serializer = self.serializer_class(billing_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return ApiResponse.success(serializer.data, "账单信息更新成功")
        return ApiResponse.validation_error(serializer.errors, "更新失败")

    def delete(self, request, pk):
        """删除账单信息"""
        try:
            billing_info = BillingInfo.objects.get(pk=pk, user=request.user)
            billing_info.delete()
            return ApiResponse.success(None, "账单信息删除成功")
        except BillingInfo.DoesNotExist:
            return ApiResponse.error("账单信息不存在")
