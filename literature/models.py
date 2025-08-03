from django.db import models
from api.models import User

class Journal(models.Model):
    name = models.CharField(max_length=255, verbose_name='期刊名称')
    impact_factor = models.FloatField(verbose_name='影响因子', null=True, blank=True)
    cas_partition = models.CharField(max_length=50, verbose_name='中科院分区', null=True, blank=True)
    jcr_partition = models.CharField(max_length=50, verbose_name='JCR分区', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Literature(models.Model):
    title = models.CharField(max_length=500, verbose_name='标题')
    abstract = models.TextField(verbose_name='摘要', null=True, blank=True)
    authors = models.TextField(verbose_name='作者', help_text='多个作者用逗号分隔')
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, verbose_name='期刊')
    pub_year = models.IntegerField(verbose_name='发表年份')
    pub_date = models.DateField(verbose_name='发表日期', null=True, blank=True)
    volume = models.CharField(max_length=50, verbose_name='卷号', null=True, blank=True)
    issue = models.CharField(max_length=50, verbose_name='期号', null=True, blank=True)
    pages = models.CharField(max_length=50, verbose_name='页码', null=True, blank=True)
    doi = models.CharField(max_length=100, verbose_name='DOI', unique=True, null=True, blank=True)
    pmid = models.CharField(max_length=100, verbose_name='PMID', unique=True, null=True, blank=True)
    keywords = models.TextField(verbose_name='关键词', null=True, blank=True, help_text='多个关键词用分号分隔')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    def __str__(self):
        return self.title

class LiteratureUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE, verbose_name='文献')
    rating = models.IntegerField(verbose_name='评级', null=True, blank=True, help_text='1-5星')
    notes = models.TextField(verbose_name='备注', null=True, blank=True)
    is_favorite = models.BooleanField(default=False, verbose_name='是否收藏')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        unique_together = ('user', 'literature')
        
    def __str__(self):
        return f'{self.user.username} - {self.literature.title}'
