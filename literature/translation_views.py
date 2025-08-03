from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .translation_service import translation_service, simple_translation_service
from .utils import ApiResponse

class TranslationView(APIView):
    """文献翻译API"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """翻译文本"""
        text = request.data.get('text', '').strip()
        target_lang = request.data.get('target_lang', 'zh')
        source_lang = request.data.get('source_lang', 'auto')
        use_cache = request.data.get('use_cache', True)
        
        if not text:
            return Response(
                ApiResponse.error("翻译文本不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 检查是否配置了翻译服务
            from django.conf import settings
            has_translation_config = all([
                hasattr(settings, 'BAIDU_APP_ID'),
                hasattr(settings, 'BAIDU_APP_KEY'),
                hasattr(settings, 'BAIDU_SECRET_KEY')
            ])
            
            if has_translation_config and settings.BAIDU_APP_ID:
                result = translation_service.translate_with_cache(text, target_lang, use_cache)
            else:
                result = simple_translation_service.translate_text(text, target_lang)
            
            return Response(
                ApiResponse.success(result),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"翻译失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LiteratureTranslationView(APIView):
    """文献翻译API"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """翻译整篇文献"""
        literature_data = request.data.get('literature', {})
        target_lang = request.data.get('target_lang', 'zh')
        
        if not literature_data:
            return Response(
                ApiResponse.error("文献数据不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 检查是否配置了翻译服务
            from django.conf import settings
            has_translation_config = all([
                hasattr(settings, 'BAIDU_APP_ID'),
                hasattr(settings, 'BAIDU_APP_KEY'),
                hasattr(settings, 'BAIDU_SECRET_KEY')
            ])
            
            if has_translation_config and settings.BAIDU_APP_ID:
                result = translation_service.translate_literature(literature_data, target_lang)
            else:
                result = simple_translation_service.translate_literature(literature_data, target_lang)
            
            return Response(
                ApiResponse.success(result),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"文献翻译失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BatchTranslationView(APIView):
    """批量翻译API"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """批量翻译文献"""
        literatures = request.data.get('literatures', [])
        target_lang = request.data.get('target_lang', 'zh')
        
        if not literatures:
            return Response(
                ApiResponse.error("文献列表不能为空"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # 检查是否配置了翻译服务
            from django.conf import settings
            has_translation_config = all([
                hasattr(settings, 'BAIDU_APP_ID'),
                hasattr(settings, 'BAIDU_APP_KEY'),
                hasattr(settings, 'BAIDU_SECRET_KEY')
            ])
            
            if has_translation_config and settings.BAIDU_APP_ID:
                results = translation_service.translate_batch_literatures(literatures, target_lang)
            else:
                results = [simple_translation_service.translate_literature(lit, target_lang) for lit in literatures]
            
            return Response(
                ApiResponse.success({
                    'translated_literatures': results,
                    'total': len(results),
                    'target_language': target_lang
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"批量翻译失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TranslationConfigView(APIView):
    """翻译配置检查API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """获取翻译服务配置状态"""
        try:
            from django.conf import settings
            
            config = {
                'baidu_configured': all([
                    hasattr(settings, 'BAIDU_APP_ID'),
                    hasattr(settings, 'BAIDU_APP_KEY'),
                    hasattr(settings, 'BAIDU_SECRET_KEY')
                ]),
                'baidu_app_id_configured': hasattr(settings, 'BAIDU_APP_ID') and bool(settings.BAIDU_APP_ID),
                'available_services': ['baidu', 'simple']
            }
            
            return Response(
                ApiResponse.success(config),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"获取配置失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )