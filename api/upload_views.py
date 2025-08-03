from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import os
import uuid
import mimetypes
from .utils import ApiResponse

class FileUploadView(APIView):
    """文件上传API视图"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    ALLOWED_FILE_TYPES = {
        'pdf': ['application/pdf'],
        'image': ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
        'excel': [
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/csv'
        ],
        'word': [
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
    }
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    def validate_file(self, file):
        """验证文件类型和大小"""
        if file.size > self.MAX_FILE_SIZE:
            return False, "文件大小不能超过50MB"
            
        file_type = mimetypes.guess_type(file.name)[0]
        if not file_type:
            return False, "无法识别文件类型"
            
        # 检查文件类型
        allowed_types = []
        for types in self.ALLOWED_FILE_TYPES.values():
            allowed_types.extend(types)
            
        if file_type not in allowed_types:
            return False, f"不支持的文件类型: {file_type}"
            
        return True, None
    
    def generate_filename(self, original_filename):
        """生成唯一文件名"""
        ext = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        return f"{unique_id}{ext}"
    
    def post(self, request):
        """处理文件上传"""
        if 'file' not in request.FILES:
            return ApiResponse.error("未找到上传文件", status.HTTP_400_BAD_REQUEST)
            
        file = request.FILES['file']
        file_type = request.data.get('type', 'general')
        
        # 验证文件
        is_valid, error_msg = self.validate_file(file)
        if not is_valid:
            return ApiResponse.error(error_msg, status.HTTP_400_BAD_REQUEST)
        
        try:
            # 生成文件名和路径
            filename = self.generate_filename(file.name)
            
            # 根据文件类型设置存储路径
            if file_type == 'literature':
                upload_path = f"literatures/{filename}"
            elif file_type == 'avatar':
                upload_path = f"avatars/{filename}"
            elif file_type == 'community':
                upload_path = f"community/{filename}"
            else:
                upload_path = f"uploads/{filename}"
            
            # 保存文件
            file_path = default_storage.save(upload_path, ContentFile(file.read()))
            
            # 如果是图片，生成缩略图
            if file.content_type and file.content_type.startswith('image'):
                self.create_thumbnail(file_path)
            
            return ApiResponse.success({
                "filename": file.name,
                "file_path": file_path,
                "file_size": file.size,
                "file_url": f"{settings.MEDIA_URL}{file_path}",
                "upload_time": file_path
            }, "文件上传成功")
            
        except Exception as e:
            return ApiResponse.error(f"文件上传失败: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create_thumbnail(self, file_path):
        """为图片创建缩略图"""
        try:
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            thumb_path = file_path.replace('.', '_thumb.')
            
            with Image.open(full_path) as img:
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                thumb_full_path = os.path.join(settings.MEDIA_ROOT, thumb_path)
                img.save(thumb_full_path)
                
        except Exception as e:
            print(f"创建缩略图失败: {e}")


class FileDeleteView(APIView):
    """文件删除API视图"""
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, file_path):
        """删除文件"""
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                
                # 同时删除缩略图
                thumb_path = file_path.replace('.', '_thumb.')
                if default_storage.exists(thumb_path):
                    default_storage.delete(thumb_path)
                    
                return ApiResponse.success(None, "文件删除成功")
            else:
                return ApiResponse.error("文件不存在", status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return ApiResponse.error(f"文件删除失败: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)