from rest_framework import serializers
from .models import User, UserProfile, BillingInfo, Literature

class UserRegistrationSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, help_text='用户密码')

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'nickname')
        extra_kwargs = {
            'username': {'help_text': '用户名'},
            'email': {'help_text': '用户邮箱'},
            'nickname': {'help_text': '用户昵称'},
        }

    def create(self, validated_data):
        """创建新用户"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname', '')
        )
        # 创建用户个人资料
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """用户个人资料序列化器"""
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('id', 'user')


class BillingInfoSerializer(serializers.ModelSerializer):
    """账单信息序列化器"""
    
    class Meta:
        model = BillingInfo
        fields = '__all__'
        read_only_fields = ('id', 'user')


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    profile = UserProfileSerializer(read_only=True)
    billing_infos = BillingInfoSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'avatar', 'points', 'vip_level', 'is_verified', 'phone', 'created_at', 'profile', 'billing_infos')
        read_only_fields = ('id', 'points', 'created_at')


class LiteratureSerializer(serializers.ModelSerializer):
    """文献序列化器"""
    uploaded_by = UserDetailSerializer(read_only=True)
    
    class Meta:
        model = Literature
        fields = '__all__'
        read_only_fields = ('id', 'uploaded_by', 'view_count', 'download_count', 'created_at', 'updated_at')
