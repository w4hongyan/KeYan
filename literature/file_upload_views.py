from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .file_upload_service import file_upload_service
from .utils import ApiResponse

class FileUploadView(APIView):
    """文件上传API"""
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        """上传文件"""
        file = request.FILES.get('file')
        file_type = request.data.get('type', 'general')
        
        if not file:
            return Response(
                ApiResponse.error("未提供文件"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = file_upload_service.upload_file(file, file_type)
            
            if 'error' in result:
                return Response(
                    ApiResponse.error(result['error']),
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(
                ApiResponse.success(result['file_info'], "文件上传成功"),
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"文件上传失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FileListView(APIView):
    """文件列表API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """获取文件列表"""
        try:
            limit = int(request.query_params.get('limit', 50))
            files = file_upload_service.get_uploaded_files(limit)
            
            return Response(
                ApiResponse.success({
                    'files': files,
                    'total': len(files)
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"获取文件列表失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FileDeleteView(APIView):
    """文件删除API"""
    permission_classes = [AllowAny]
    
    def delete(self, request, filename):
        """删除文件"""
        try:
            file_path = file_upload_service.upload_dir + '/' + filename
            result = file_upload_service.delete_file(file_path)
            
            if 'error' in result:
                return Response(
                    ApiResponse.error(result['error']),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                ApiResponse.success(None, "文件删除成功"),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"文件删除失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FileUploadConfigView(APIView):
    """文件上传配置API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """获取文件上传配置"""
        try:
            config = {
                'max_file_size': file_upload_service.MAX_FILE_SIZE,
                'max_image_size': file_upload_service.MAX_IMAGE_SIZE,
                'allowed_image_types': list(file_upload_service.ALLOWED_IMAGE_TYPES.keys()),
                'allowed_document_types': list(file_upload_service.ALLOWED_DOCUMENT_TYPES.keys()),
                'upload_dir': 'media/uploads'
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