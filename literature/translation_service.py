import requests
import json
import hashlib
import urllib.parse
import time
import random
from typing import Dict, List, Optional
from django.conf import settings

class TranslationService:
    """文献翻译服务类"""
    
    def __init__(self):
        self.baidu_app_id = getattr(settings, 'BAIDU_APP_ID', '')
        self.baidu_app_key = getattr(settings, 'BAIDU_APP_KEY', '')
        self.baidu_secret_key = getattr(settings, 'BAIDU_SECRET_KEY', '')
        
    def translate_text(self, text: str, target_lang: str = 'zh', source_lang: str = 'auto') -> Dict:
        """翻译文本"""
        if not text.strip():
            return {'translated_text': '', 'source_lang': source_lang, 'target_lang': target_lang}
        
        # 使用百度翻译API
        return self._baidu_translate(text, source_lang, target_lang)
    
    def _baidu_translate(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """百度翻译API实现"""
        if not all([self.baidu_app_id, self.baidu_app_key, self.baidu_secret_key]):
            return {'error': '翻译服务未配置', 'translated_text': text}
        
        try:
            url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
            
            # 生成随机数
            salt = str(random.randint(32768, 65536))
            
            # 生成签名
            sign_str = f"{self.baidu_app_id}{text}{salt}{self.baidu_secret_key}"
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
            
            # 构建参数
            params = {
                'q': text,
                'from': source_lang,
                'to': target_lang,
                'appid': self.baidu_app_id,
                'salt': salt,
                'sign': sign
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if 'error_code' in result:
                return {'error': result.get('error_msg', '翻译失败'), 'translated_text': text}
            
            if 'trans_result' in result and result['trans_result']:
                translated_text = result['trans_result'][0]['dst']
                detected_lang = result.get('from', source_lang)
                
                return {
                    'translated_text': translated_text,
                    'source_lang': detected_lang,
                    'target_lang': target_lang,
                    'original_text': text
                }
            
            return {'error': '翻译结果为空', 'translated_text': text}
            
        except Exception as e:
            return {'error': f'翻译请求失败: {str(e)}', 'translated_text': text}
    
    def translate_literature(self, literature_data: Dict, target_lang: str = 'zh') -> Dict:
        """翻译整篇文献"""
        translated = {
            'title': '',
            'abstract': '',
            'keywords': [],
            'authors': [],
            'journal': '',
            'original_data': literature_data
        }
        
        # 翻译标题
        if literature_data.get('title'):
            title_result = self.translate_text(literature_data['title'], target_lang)
            translated['title'] = title_result.get('translated_text', literature_data['title'])
        
        # 翻译摘要
        if literature_data.get('abstract'):
            abstract_result = self.translate_text(literature_data['abstract'], target_lang)
            translated['abstract'] = abstract_result.get('translated_text', literature_data['abstract'])
        
        # 翻译关键词
        if literature_data.get('keywords'):
            translated_keywords = []
            for keyword in literature_data['keywords']:
                keyword_result = self.translate_text(keyword, target_lang)
                translated_keywords.append(keyword_result.get('translated_text', keyword))
            translated['keywords'] = translated_keywords
        
        # 翻译作者（通常不需要翻译，保持原文）
        translated['authors'] = literature_data.get('authors', [])
        
        # 翻译期刊名称
        if literature_data.get('journal'):
            journal_result = self.translate_text(literature_data['journal'], target_lang)
            translated['journal'] = journal_result.get('translated_text', literature_data['journal'])
        
        return translated
    
    def translate_batch_literatures(self, literatures: List[Dict], target_lang: str = 'zh') -> List[Dict]:
        """批量翻译文献"""
        translated_literatures = []
        
        for literature in literatures:
            translated = self.translate_literature(literature, target_lang)
            translated_literatures.append(translated)
        
        return translated_literatures
    
    def get_translation_cache_key(self, text: str, target_lang: str) -> str:
        """生成翻译缓存key"""
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        return f"translation_{target_lang}_{text_hash}"
    
    def translate_with_cache(self, text: str, target_lang: str = 'zh', use_cache: bool = True) -> Dict:
        """带缓存的翻译"""
        if use_cache:
            from django.core.cache import cache
            cache_key = self.get_translation_cache_key(text, target_lang)
            cached_result = cache.get(cache_key)
            
            if cached_result:
                return cached_result
        
        result = self.translate_text(text, target_lang)
        
        if use_cache and 'error' not in result:
            from django.core.cache import cache
            cache_key = self.get_translation_cache_key(text, target_lang)
            cache.set(cache_key, result, 3600)  # 缓存1小时
        
        return result

class SimpleTranslationService:
    """简单的翻译服务（用于测试或备用）"""
    
    def translate_text(self, text: str, target_lang: str = 'zh') -> Dict:
        """简单翻译（返回原文）"""
        return {
            'translated_text': text,
            'source_lang': 'auto',
            'target_lang': target_lang,
            'note': '这是测试翻译服务，实际翻译功能需要配置API密钥'
        }
    
    def translate_literature(self, literature_data: Dict, target_lang: str = 'zh') -> Dict:
        """简单翻译整篇文献"""
        return {
            'title': literature_data.get('title', ''),
            'abstract': literature_data.get('abstract', ''),
            'keywords': literature_data.get('keywords', []),
            'authors': literature_data.get('authors', []),
            'journal': literature_data.get('journal', ''),
            'note': '这是测试翻译服务，实际翻译功能需要配置API密钥',
            'original_data': literature_data
        }

# 创建全局实例
translation_service = TranslationService()
simple_translation_service = SimpleTranslationService()