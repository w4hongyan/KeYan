from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    color = models.CharField(max_length=7, default='#007bff', verbose_name='标签颜色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name='问题标题')
    content = models.TextField(verbose_name='问题内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name='提问者')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    
    # 统计字段
    upvote_count = models.PositiveIntegerField(default=0, verbose_name='赞同次数')
    downvote_count = models.PositiveIntegerField(default=0, verbose_name='反对次数')
    collect_count = models.PositiveIntegerField(default=0, verbose_name='收藏次数')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = '问题'
        verbose_name_plural = '问题'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='问题')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', verbose_name='回答者')
    content = models.TextField(verbose_name='回答内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 统计字段
    upvote_count = models.PositiveIntegerField(default=0, verbose_name='赞同次数')
    downvote_count = models.PositiveIntegerField(default=0, verbose_name='反对次数')
    is_accepted = models.BooleanField(default=False, verbose_name='是否被采纳')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['question', 'created_at']),
            models.Index(fields=['author', 'created_at']),
        ]
        verbose_name = '回答'
        verbose_name_plural = '回答'

class Vote(models.Model):
    VOTE_TYPES = [
        ('up', '赞同'),
        ('down', '反对'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField(verbose_name='对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPES, verbose_name='投票类型')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        verbose_name = '投票'
        verbose_name_plural = '投票'

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='内容类型')
    object_id = models.PositiveIntegerField(verbose_name='对象ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        verbose_name = '收藏'
        verbose_name_plural = '收藏'