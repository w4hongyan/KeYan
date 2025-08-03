import os
import uuid
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import mimetypes
from PIL import Image
import json

class FileUploadService:
    """文件上传服务类"""
    
    ALLOWED_IMAGE_TYPES = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp'
    }
    
    ALLOWED_DOCUMENT_TYPES = {
        'application/pdf': '.pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.ms-excel': '.xls'
    }
    
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    
    def __init__(self):
        self.upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        self.ensure_upload_dir()
    
    def ensure_upload_dir(self):
        """确保上传目录存在"""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir, exist_ok=True)
    
    def validate_file_type(self, file) -> bool:
        """验证文件类型"""
        try:
            file_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
            file.seek(0)  # 重置文件指针
            
            return (file_type in self.ALLOWED_IMAGE_TYPES or 
                   file_type in self.ALLOWED_DOCUMENT_TYPES)
        except Exception:
            return False
    
    def validate_file_size(self, file, max_size: int = None) -> bool:
        """验证文件大小"""
        if max_size is None:
            max_size = self.MAX_FILE_SIZE
        
        return file.size <= max_size
    
    def generate_filename(self, original_filename: str, file_type: str) -> str:
        """生成唯一文件名"""
        ext = os.path.splitext(original_filename)[1].lower()
        if not ext:
            # 根据文件类型添加扩展名
            ext = self.ALLOWED_IMAGE_TYPES.get(file_type, '') or \
                  self.ALLOWED_DOCUMENT_TYPES.get(file_type, '')
        
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{timestamp}_{unique_id}{ext}"
    
    def calculate_file_hash(self, file) -> str:
        """计算文件哈希值"""
        hasher = hashlib.md5()
        for chunk in file.chunks():
            hasher.update(chunk)
        return hasher.hexdigest()
    
    def upload_file(self, file, file_type: str = 'general') -> Dict:
        """上传文件"""
        try:
            # 验证文件
            if not self.validate_file_type(file):
                return {'error': '不支持的文件类型'}
            
            # 根据文件类型设置大小限制
            max_size = self.MAX_IMAGE_SIZE if file_type == 'image' else self.MAX_FILE_SIZE
            if not self.validate_file_size(file, max_size):
                return {'error': f'文件大小超过限制（最大{max_size//1024//1024}MB）'}
            
            # 检测实际文件类型
            actual_file_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
            file.seek(0)
            
            # 生成文件名
            filename = self.generate_filename(file.name, actual_file_type)
            file_path = os.path.join(self.upload_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # 计算文件哈希
            file_hash = self.calculate_file_hash(file)
            
            # 获取文件信息
            file_info = {
                'filename': filename,
                'original_name': file.name,
                'file_path': file_path,
                'file_size': file.size,
                'file_type': actual_file_type,
                'file_hash': file_hash,
                'upload_time': datetime.now().isoformat(),
                'relative_path': f"uploads/{filename}"
            }
            
            # 如果是PDF，提取额外信息
            if actual_file_type == 'application/pdf':
                pdf_info = self.extract_pdf_info(file_path)
                file_info.update(pdf_info)
            
            # 如果是图片，生成缩略图
            elif actual_file_type in self.ALLOWED_IMAGE_TYPES:
                thumbnail_path = self.create_thumbnail(file_path)
                file_info['thumbnail_path'] = thumbnail_path
            
            return {'success': True, 'file_info': file_info}
            
        except Exception as e:
            return {'error': f'文件上传失败: {str(e)}'}
    
    def extract_pdf_info(self, file_path: str) -> Dict:
        """提取PDF信息"""
        return {'pdf_pages': 0, 'pdf_title': '', 'pdf_author': '', 'pdf_subject': ''}
    
    def create_thumbnail(self, file_path: str, size: tuple = (300, 300)) -> str:
        """创建图片缩略图"""
        try:
            with Image.open(file_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # 生成缩略图文件名
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                thumbnail_name = f"thumb_{base_name}.jpg"
                thumbnail_path = os.path.join(self.upload_dir, thumbnail_name)
                
                # 保存缩略图
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(thumbnail_path, 'JPEG', quality=85)
                
                return thumbnail_path
                
        except Exception as e:
            print(f"创建缩略图失败: {e}")
            return ''
    
    def delete_file(self, file_path: str) -> Dict:
        """删除文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                
                # 同时删除缩略图
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                thumbnail_path = os.path.join(self.upload_dir, f"thumb_{base_name}.jpg")
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
                
                return {'success': True, 'message': '文件删除成功'}
            else:
                return {'error': '文件不存在'}
                
        except Exception as e:
            return {'error': f'文件删除失败: {str(e)}'}
    
    def get_uploaded_files(self, limit: int = 50) -> List[Dict]:
        """获取已上传文件列表"""
        try:
            files = []
            for filename in os.listdir(self.upload_dir):
                if filename.startswith('thumb_'):
                    continue
                    
                file_path = os.path.join(self.upload_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    files.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'upload_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'relative_path': f"uploads/{filename}"
                    })
            
            # 按上传时间排序
            files.sort(key=lambda x: x['upload_time'], reverse=True)
            return files[:limit]
            
        except Exception:
            return []

# 创建全局实例
file_upload_service = FileUploadService()