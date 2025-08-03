from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
import re
import math
from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
from .models import Literature, LiteratureUser

class PlagiarismCheckViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def check_similarity(self, request):
        """检查文本相似度"""
        try:
            text1 = request.data.get('text1', '')
            text2 = request.data.get('text2', '')
            
            if not text1 or not text2:
                return Response({
                    'success': False,
                    'message': '请输入两段文本进行比较'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 计算相似度
            similarity = self.calculate_similarity(text1, text2)
            
            # 详细分析
            analysis = self.analyze_text_similarity(text1, text2)
            
            result = {
                'similarity_score': similarity,
                'similarity_percentage': round(similarity * 100, 2),
                'risk_level': self.get_risk_level(similarity),
                'analysis': analysis,
                'recommendations': self.get_recommendations(similarity)
            }

            return Response({
                'success': True,
                'data': result
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def check_literature(self, request):
        """检查文献与数据库的相似度"""
        try:
            literature_id = request.data.get('literature_id')
            text = request.data.get('text')
            
            if not literature_id and not text:
                return Response({
                    'success': False,
                    'message': '请提供文献ID或直接提供文本'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取待检查文本
            if literature_id:
                try:
                    literature = Literature.objects.get(id=literature_id)
                    text_to_check = literature.abstract or literature.title
                except Literature.DoesNotExist:
                    return Response({
                        'success': False,
                        'message': '文献不存在'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                text_to_check = text

            # 获取用户所有文献进行对比
            user_literatures = LiteratureUser.objects.filter(
                user=request.user
            ).select_related('literature')

            results = []
            for lit_user in user_literatures:
                literature = lit_user.literature
                comparison_text = literature.abstract or literature.title
                
                if comparison_text:
                    similarity = self.calculate_similarity(text_to_check, comparison_text)
                    if similarity > 0.1:  # 只显示相似度>10%的结果
                        results.append({
                            'literature_id': literature.id,
                            'title': literature.title,
                            'authors': literature.authors,
                            'similarity': similarity,
                            'similarity_percentage': round(similarity * 100, 2),
                            'risk_level': self.get_risk_level(similarity)
                        })

            # 按相似度排序
            results.sort(key=lambda x: x['similarity'], reverse=True)

            return Response({
                'success': True,
                'data': {
                    'total_checked': len(results),
                    'high_risk': len([r for r in results if r['similarity'] > 0.7]),
                    'medium_risk': len([r for r in results if 0.4 <= r['similarity'] <= 0.7]),
                    'low_risk': len([r for r in results if r['similarity'] < 0.4]),
                    'results': results[:20]  # 返回前20个最相似的结果
                }
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def check_url(self, request):
        """检查网页内容相似度"""
        try:
            url = request.data.get('url')
            text = request.data.get('text')
            
            if not url or not text:
                return Response({
                    'success': False,
                    'message': '请提供URL和待检查文本'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 获取网页内容
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取文本内容
            web_text = soup.get_text()
            web_text = re.sub(r'\s+', ' ', web_text).strip()

            # 计算相似度
            similarity = self.calculate_similarity(text, web_text)
            
            return Response({
                'success': True,
                'data': {
                    'similarity_score': similarity,
                    'similarity_percentage': round(similarity * 100, 2),
                    'risk_level': self.get_risk_level(similarity),
                    'web_content_length': len(web_text),
                    'text_length': len(text)
                }
            })

        except requests.RequestException:
            return Response({
                'success': False,
                'message': '无法访问指定的URL'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """计算两段文本的相似度"""
        # 预处理文本
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        if not text1 or not text2:
            return 0.0

        # 使用SequenceMatcher计算相似度
        similarity = SequenceMatcher(None, text1, text2).ratio()
        
        # 计算Jaccard相似度作为补充
        jaccard_similarity = self.jaccard_similarity(text1, text2)
        
        # 综合两种算法的结果
        final_similarity = (similarity + jaccard_similarity) / 2
        
        return min(final_similarity, 1.0)

    def preprocess_text(self, text: str) -> str:
        """文本预处理"""
        # 转换为小写
        text = text.lower()
        
        # 移除标点符号和特殊字符
        text = re.sub(r'[^\w\s]', '', text)
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """计算Jaccard相似度"""
        set1 = set(text1.split())
        set2 = set(text2.split())
        
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0

    def analyze_text_similarity(self, text1: str, text2: str) -> dict:
        """详细分析文本相似度"""
        # 分句处理
        sentences1 = self.split_sentences(text1)
        sentences2 = self.split_sentences(text2)
        
        # 计算句子级别的相似度
        sentence_matches = []
        for sent1 in sentences1:
            best_match = None
            best_score = 0
            for sent2 in sentences2:
                score = SequenceMatcher(None, sent1, sent2).ratio()
                if score > best_score:
                    best_score = score
                    best_match = sent2
            
            if best_score > 0.8:
                sentence_matches.append({
                    'original': sent1,
                    'matched': best_match,
                    'similarity': round(best_score, 2)
                })
        
        # 关键词提取和匹配
        keywords1 = self.extract_keywords(text1)
        keywords2 = self.extract_keywords(text2)
        
        common_keywords = set(keywords1).intersection(set(keywords2))
        
        return {
            'sentence_matches': sentence_matches,
            'common_keywords': list(common_keywords),
            'keyword_similarity': len(common_keywords) / max(len(keywords1), len(keywords2), 1),
            'sentence_coverage': len(sentence_matches) / max(len(sentences1), 1)
        }

    def split_sentences(self, text: str) -> list:
        """将文本分句"""
        # 简单的分句逻辑
        sentences = re.split(r'[.!?。！？]', text)
        return [s.strip() for s in sentences if s.strip()]

    def extract_keywords(self, text: str) -> list:
        """提取关键词"""
        # 简单的关键词提取：移除停用词后取高频词
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # 返回前10个高频词
        from collections import Counter
        word_counts = Counter(words)
        return [word for word, count in word_counts.most_common(10)]

    def get_risk_level(self, similarity: float) -> str:
        """根据相似度返回风险等级"""
        if similarity >= 0.8:
            return 'high'
        elif similarity >= 0.5:
            return 'medium'
        else:
            return 'low'

    def get_recommendations(self, similarity: float) -> list:
        """根据相似度提供建议"""
        recommendations = []
        
        if similarity >= 0.8:
            recommendations.extend([
                '文本相似度过高，建议重新撰写',
                '检查引用格式是否正确',
                '考虑增加原创性内容'
            ])
        elif similarity >= 0.5:
            recommendations.extend([
                '文本相似度中等，建议适当修改',
                '增加更多原创分析和观点',
                '确保引用内容已正确标注'
            ])
        else:
            recommendations.extend([
                '文本相似度较低，符合原创要求',
                '继续保持良好的学术规范'
            ])
            
        return recommendations