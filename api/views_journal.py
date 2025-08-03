from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
import requests
import json
from typing import Dict, List
import re
from datetime import datetime, timedelta

class JournalImpactViewSet(viewsets.ViewSet):
    """期刊影响因子查询API"""
    
    permission_classes = [IsAuthenticated]
    
    # 期刊缩写映射
    JOURNAL_ABBREVIATIONS = {
        'Nature': 'NAT',
        'Science': 'SCI',
        'Cell': 'CELL',
        'Nature Medicine': 'NAT MED',
        'Nature Biotechnology': 'NAT BIOTECHNOL',
        'Science Translational Medicine': 'SCI TRANSL MED',
        'Cell Stem Cell': 'CELL STEM CELL',
        'Nature Communications': 'NAT COMMUN',
        'Science Advances': 'SCI ADV',
        'Cell Reports': 'CELL REP',
        'PNAS': 'P NATL ACAD SCI USA',
        'PLOS ONE': 'PLOS ONE',
        'Scientific Reports': 'SCI REP-UK',
    }
    
    @action(detail=False, methods=['GET'])
    def search_journal(self, request):
        """搜索期刊信息"""
        query = request.query_params.get('query', '').strip()
        if not query:
            return Response({'error': '请输入期刊名称'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 缓存键
        cache_key = f'journal_search_{query}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)
        
        # 模拟期刊搜索（实际应用中应调用真实API）
        journals = self._search_journals(query)
        
        # 缓存1小时
        cache.set(cache_key, journals, 3600)
        
        return Response({
            'query': query,
            'results': journals,
            'count': len(journals)
        })
    
    @action(detail=False, methods=['GET'])
    def get_impact_factor(self, request):
        """获取期刊影响因子"""
        journal_name = request.query_params.get('journal', '').strip()
        year = request.query_params.get('year', str(datetime.now().year - 1))
        
        if not journal_name:
            return Response({'error': '请输入期刊名称'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 缓存键
        cache_key = f'impact_factor_{journal_name}_{year}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)
        
        # 获取影响因子数据
        impact_data = self._get_impact_factor_data(journal_name, year)
        
        # 缓存6小时
        cache.set(cache_key, impact_data, 21600)
        
        return Response(impact_data)
    
    @action(detail=False, methods=['GET'])
    def get_journal_rankings(self, request):
        """获取期刊排名"""
        field = request.query_params.get('field', 'all')
        limit = int(request.query_params.get('limit', 50))
        
        # 缓存键
        cache_key = f'journal_rankings_{field}_{limit}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result)
        
        # 获取排名数据
        rankings = self._get_journal_rankings(field, limit)
        
        # 缓存12小时
        cache.set(cache_key, rankings, 43200)
        
        return Response({
            'field': field,
            'rankings': rankings,
            'count': len(rankings)
        })
    
    @action(detail=False, methods=['POST'])
    def batch_query(self, request):
        """批量查询期刊影响因子"""
        journal_names = request.data.get('journals', [])
        year = request.data.get('year', str(datetime.now().year - 1))
        
        if not journal_names:
            return Response({'error': '请提供期刊列表'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        for journal_name in journal_names:
            cache_key = f'impact_factor_{journal_name}_{year}'
            cached_result = cache.get(cache_key)
            
            if cached_result:
                results.append(cached_result)
            else:
                impact_data = self._get_impact_factor_data(journal_name, year)
                cache.set(cache_key, impact_data, 21600)
                results.append(impact_data)
        
        return Response({
            'year': year,
            'results': results,
            'count': len(results)
        })
    
    def _search_journals(self, query: str) -> List[Dict]:
        """搜索期刊（模拟数据）"""
        # 这里应该调用真实的期刊数据库API
        mock_journals = [
            {
                'name': 'Nature',
                'abbreviation': 'NAT',
                'issn': '0028-0836',
                'publisher': 'Nature Publishing Group',
                'field': 'Multidisciplinary',
                'impact_factor_2023': 64.8,
                'rank': 1
            },
            {
                'name': 'Science',
                'abbreviation': 'SCI',
                'issn': '0036-8075',
                'publisher': 'American Association for the Advancement of Science',
                'field': 'Multidisciplinary',
                'impact_factor_2023': 63.7,
                'rank': 2
            },
            {
                'name': 'Nature Medicine',
                'abbreviation': 'NAT MED',
                'issn': '1078-8956',
                'publisher': 'Nature Publishing Group',
                'field': 'Medicine',
                'impact_factor_2023': 87.2,
                'rank': 1
            },
            {
                'name': 'Cell',
                'abbreviation': 'CELL',
                'issn': '0092-8674',
                'publisher': 'Cell Press',
                'field': 'Biology',
                'impact_factor_2023': 66.8,
                'rank': 1
            }
        ]
        
        # 简单的模糊匹配
        query_lower = query.lower()
        filtered = [
            journal for journal in mock_journals
            if query_lower in journal['name'].lower() or 
               query_lower in journal['abbreviation'].lower()
        ]
        
        return filtered
    
    def _get_impact_factor_data(self, journal_name: str, year: str) -> Dict:
        """获取期刊影响因子数据（模拟数据）"""
        # 这里应该调用真实的期刊影响因子API
        mock_data = {
            'Nature': {
                '2023': {'impact_factor': 64.8, 'total_cites': 800000, 'articles': 850},
                '2022': {'impact_factor': 69.5, 'total_cites': 780000, 'articles': 820},
                '2021': {'impact_factor': 62.7, 'total_cites': 750000, 'articles': 800}
            },
            'Science': {
                '2023': {'impact_factor': 63.7, 'total_cites': 750000, 'articles': 780},
                '2022': {'impact_factor': 65.2, 'total_cites': 730000, 'articles': 760},
                '2021': {'impact_factor': 60.8, 'total_cites': 710000, 'articles': 750}
            },
            'Cell': {
                '2023': {'impact_factor': 66.8, 'total_cites': 400000, 'articles': 350},
                '2022': {'impact_factor': 68.2, 'total_cites': 390000, 'articles': 340},
                '2021': {'impact_factor': 65.1, 'total_cites': 380000, 'articles': 335}
            }
        }
        
        journal_key = next((k for k in mock_data.keys() if k.lower() in journal_name.lower()), journal_name)
        
        if journal_key in mock_data and year in mock_data[journal_key]:
            return {
                'journal': journal_name,
                'year': year,
                'impact_factor': mock_data[journal_key][year]['impact_factor'],
                'total_cites': mock_data[journal_key][year]['total_cites'],
                'articles': mock_data[journal_key][year]['articles'],
                'cites_per_article': round(
                    mock_data[journal_key][year]['total_cites'] / mock_data[journal_key][year]['articles'], 2
                ),
                'last_updated': datetime.now().isoformat()
            }
        else:
            return {
                'journal': journal_name,
                'year': year,
                'error': '未找到该期刊的影响因子数据',
                'suggestion': '请检查期刊名称是否正确，或尝试其他年份'
            }
    
    def _get_journal_rankings(self, field: str, limit: int) -> List[Dict]:
        """获取期刊排名（模拟数据）"""
        rankings = [
            {
                'rank': 1,
                'name': 'Nature',
                'abbreviation': 'NAT',
                'impact_factor_2023': 64.8,
                'field': 'Multidisciplinary',
                'quartile': 'Q1'
            },
            {
                'rank': 2,
                'name': 'Science',
                'abbreviation': 'SCI',
                'impact_factor_2023': 63.7,
                'field': 'Multidisciplinary',
                'quartile': 'Q1'
            },
            {
                'rank': 3,
                'name': 'Nature Medicine',
                'abbreviation': 'NAT MED',
                'impact_factor_2023': 87.2,
                'field': 'Medicine',
                'quartile': 'Q1'
            },
            {
                'rank': 4,
                'name': 'Cell',
                'abbreviation': 'CELL',
                'impact_factor_2023': 66.8,
                'field': 'Biology',
                'quartile': 'Q1'
            }
        ]
        
        if field != 'all':
            rankings = [r for r in rankings if r['field'].lower() == field.lower()]
        
        return rankings[:limit]