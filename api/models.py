from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='邮箱')
    nickname = models.CharField(max_length=150, blank=True, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    points = models.IntegerField(default=0, verbose_name='积分')
    vip_level = models.IntegerField(default=0, choices=[(0, '普通用户'), (1, 'VIP'), (2, 'SVIP')], verbose_name='会员等级')
    is_verified = models.BooleanField(default=False, verbose_name='是否认证')
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # Add related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    name = models.CharField(max_length=100, blank=True, verbose_name='姓名')
    education_experience = models.TextField(blank=True, verbose_name='教育经历')
    research_field = models.CharField(max_length=255, blank=True, verbose_name='研究领域')
    location = models.CharField(max_length=255, blank=True, verbose_name='所在地')
    institution = models.CharField(max_length=255, blank=True, verbose_name='所在机构')
    department = models.CharField(max_length=255, blank=True, verbose_name='所在部门')
    title = models.CharField(max_length=100, blank=True, verbose_name='职称')
    receive_review_invitations = models.BooleanField(default=False, verbose_name='同意收到审稿邀请')
    receive_guidance_invitations = models.BooleanField(default=False, verbose_name='同意收到科研辅导邀请')
    receive_cooperation_invitations = models.BooleanField(default=False, verbose_name='同意收到科研合作邀请')

class Literature(models.Model):
    title = models.CharField(max_length=500, verbose_name='标题')
    authors = models.TextField(verbose_name='作者')
    abstract = models.TextField(blank=True, verbose_name='摘要')
    keywords = models.TextField(blank=True, verbose_name='关键词')
    doi = models.CharField(max_length=255, blank=True, verbose_name='DOI')
    url = models.URLField(blank=True, verbose_name='链接')
    publication_date = models.DateField(null=True, blank=True, verbose_name='发表日期')
    journal = models.CharField(max_length=255, blank=True, verbose_name='期刊')
    volume = models.CharField(max_length=50, blank=True, verbose_name='卷')
    issue = models.CharField(max_length=50, blank=True, verbose_name='期')
    pages = models.CharField(max_length=50, blank=True, verbose_name='页码')
    category = models.CharField(max_length=100, verbose_name='领域分类')
    file_path = models.FileField(upload_to='literatures/', null=True, blank=True, verbose_name='文件路径')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='literatures', verbose_name='上传用户')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    download_count = models.IntegerField(default=0, verbose_name='下载次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class BillingInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_infos', verbose_name='用户')
    institution_name = models.CharField(max_length=255, verbose_name='机构名称')
    tax_id = models.CharField(max_length=100, verbose_name='纳税识别号')
    address = models.CharField(max_length=255, verbose_name='地址')
    phone = models.CharField(max_length=20, verbose_name='电话')
    bank_name = models.CharField(max_length=100, verbose_name='开户行')
    bank_account = models.CharField(max_length=100, verbose_name='账号')

    def __str__(self):
        return self.institution_name
