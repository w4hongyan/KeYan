from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class CooperationType(models.TextChoices):
    MUTUAL_HELP = 'mutual', '互助'
    COLLABORATION = 'collab', '合作'

class CooperationStatus(models.TextChoices):
    PENDING = 'pending', '待接单'
    IN_PROGRESS = 'progress', '进行中'
    COMPLETED = 'completed', '已完成'
    CANCELLED = 'cancelled', '已取消'

class CooperationPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    cooperation_type = models.CharField(max_length=10, choices=CooperationType.choices, verbose_name='合作类型')
    
    # 发布者信息
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cooperation_posts', verbose_name='发布者')
    
    # 需求详情
    requirements = models.JSONField(default=dict, help_text="结构化需求描述", verbose_name='需求详情')
    reward_description = models.TextField(help_text="酬劳或合作条件", verbose_name='酬劳描述')
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='预算')
    
    # 技能要求
    required_skills = models.JSONField(default=list, help_text="所需技能列表", verbose_name='所需技能')
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', '初级'),
            ('intermediate', '中级'),
            ('advanced', '高级'),
            ('expert', '专家'),
        ],
        default='intermediate',
        verbose_name='难度级别'
    )
    
    # 状态管理
    status = models.CharField(
        max_length=10,
        choices=CooperationStatus.choices,
        default=CooperationStatus.PENDING,
        verbose_name='状态'
    )
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='截止日期')
    expected_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="预期完成时间（小时）",
        verbose_name='预期时长'
    )
    
    # 统计信息
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    application_count = models.PositiveIntegerField(default=0, verbose_name='申请次数')
    
    # 标签
    tags = models.JSONField(default=list, help_text="项目标签", verbose_name='标签')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['publisher', 'created_at']),
            models.Index(fields=['cooperation_type', 'status']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = '合作帖子'
        verbose_name_plural = '合作帖子'
    
    def __str__(self):
        return f"{self.title} - {self.publisher.username}"

class CooperationApplication(models.Model):
    post = models.ForeignKey(CooperationPost, on_delete=models.CASCADE, related_name='applications', verbose_name='合作帖子')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cooperation_applications', verbose_name='申请者')
    
    # 申请信息
    cover_letter = models.TextField(help_text="申请说明", verbose_name='申请信')
    proposed_solution = models.TextField(help_text="解决方案", verbose_name='解决方案')
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='报价')
    
    # 能力证明
    portfolio_url = models.URLField(null=True, blank=True, help_text="作品集链接", verbose_name='作品集链接')
    relevant_experience = models.TextField(null=True, blank=True, help_text="相关经验", verbose_name='相关经验')
    
    # 时间安排
    estimated_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="预计完成时间（小时）",
        verbose_name='预计时长'
    )
    available_start_date = models.DateField(null=True, blank=True, verbose_name='可开始日期')
    
    # 状态
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', '待审核'),
            ('accepted', '已接受'),
            ('rejected', '已拒绝'),
            ('cancelled', '已取消'),
        ],
        default='pending',
        verbose_name='状态'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    review_note = models.TextField(null=True, blank=True, verbose_name='审核备注')
    
    class Meta:
        unique_together = ['post', 'applicant']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'status']),
            models.Index(fields=['applicant', 'created_at']),
        ]
        verbose_name = '合作申请'
        verbose_name_plural = '合作申请'
    
    def __str__(self):
        return f"{self.applicant.username} - {self.post.title}"

class CooperationProgress(models.Model):
    cooperation = models.ForeignKey(
        CooperationPost,
        on_delete=models.CASCADE,
        related_name='progress_updates',
        verbose_name='合作项目'
    )
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='合作者')
    
    progress_percentage = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='进度百分比'
    )
    description = models.TextField(verbose_name='进度描述')
    
    # 交付物
    deliverables = models.JSONField(default=list, help_text="交付文件列表", verbose_name='交付物')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cooperation', 'created_at']),
        ]
        verbose_name = '合作进度'
        verbose_name_plural = '合作进度'

class CooperationReview(models.Model):
    cooperation = models.OneToOneField(
        CooperationPost,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='合作项目'
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评价者')
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='评分'
    )
    comment = models.TextField(verbose_name='评价内容')
    
    # 评价维度
    communication_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name='沟通评分'
    )
    quality_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name='质量评分'
    )
    timeliness_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name='及时性评分'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '合作评价'
        verbose_name_plural = '合作评价'

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='技能名称')
    category = models.CharField(max_length=50, verbose_name='技能分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '技能'
        verbose_name_plural = '技能'

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills', verbose_name='用户')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name='技能')
    proficiency_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', '初级'),
            ('intermediate', '中级'),
            ('advanced', '高级'),
            ('expert', '专家'),
        ],
        default='beginner',
        verbose_name='熟练度'
    )
    verified = models.BooleanField(default=False, verbose_name='已认证')
    
    class Meta:
        unique_together = ['user', 'skill']
        verbose_name = '用户技能'
        verbose_name_plural = '用户技能'