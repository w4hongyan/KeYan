from rest_framework import serializers
from .models import Journal, Literature, LiteratureUser
from api.serializers import UserRegistrationSerializer

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = '__all__'
        extra_kwargs = {
            'name': {'help_text': '期刊名称'},
            'impact_factor': {'help_text': '影响因子'},
            'cas_partition': {'help_text': '中科院分区'},
            'jcr_partition': {'help_text': 'JCR分区'},
        }

class LiteratureSerializer(serializers.ModelSerializer):
    journal_info = JournalSerializer(source='journal', read_only=True)
    
    class Meta:
        model = Literature
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'title': {'help_text': '文献标题'},
            'abstract': {'help_text': '文献摘要'},
            'authors': {'help_text': '文献作者，多个作者用逗号分隔'},
            'journal': {'help_text': '期刊ID'},
            'pub_year': {'help_text': '发表年份'},
            'pub_date': {'help_text': '发表日期'},
            'volume': {'help_text': '卷号'},
            'issue': {'help_text': '期号'},
            'pages': {'help_text': '页码'},
            'doi': {'help_text': 'DOI'},
            'pmid': {'help_text': 'PMID'},
            'keywords': {'help_text': '关键词，多个关键词用分号分隔'},
        }
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['journal_info'] = JournalSerializer(instance.journal).data
        return representation

class LiteratureUserSerializer(serializers.ModelSerializer):
    literature_info = LiteratureSerializer(source='literature', read_only=True)
    user_info = UserRegistrationSerializer(source='user', read_only=True)
    
    class Meta:
        model = LiteratureUser
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'user')
        extra_kwargs = {
            'literature': {'help_text': '文献ID'},
            'rating': {'help_text': '评级，1-5星'},
            'notes': {'help_text': '备注'},
            'is_favorite': {'help_text': '是否收藏'},
        }
        

        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['literature_info'] = LiteratureSerializer(instance.literature).data
        representation['user_info'] = UserRegistrationSerializer(instance.user).data
        return representation