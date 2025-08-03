from rest_framework.response import Response
from rest_framework import status


class ApiResponse:
    """统一API响应格式工具类"""
    
    @staticmethod
    def success(data=None, message="操作成功", code=200):
        """
        成功响应
        
        Args:
            data: 响应数据
            message: 成功消息
            code: HTTP状态码
        
        Returns:
            Response: 格式化的成功响应
        """
        return Response({
            'code': code,
            'message': message,
            'data': data,
            'success': True
        }, status=code)
    
    @staticmethod
    def error(message="操作失败", code=400, errors=None):
        """
        错误响应
        
        Args:
            message: 错误消息
            code: HTTP状态码
            errors: 详细错误信息
        
        Returns:
            Response: 格式化的错误响应
        """
        return Response({
            'code': code,
            'message': message,
            'errors': errors,
            'success': False
        }, status=code)
    
    @staticmethod
    def paginated(data, total, page=1, size=10):
        """
        分页响应
        
        Args:
            data: 数据列表
            total: 总记录数
            page: 当前页码
            size: 每页大小
        
        Returns:
            Response: 分页响应
        """
        return ApiResponse.success({
            'list': data,
            'total': total,
            'page': page,
            'size': size
        })
    
    @staticmethod
    def created(data=None, message="创建成功"):
        """创建成功响应"""
        return ApiResponse.success(data, message, status.HTTP_201_CREATED)
    
    @staticmethod
    def updated(data=None, message="更新成功"):
        """更新成功响应"""
        return ApiResponse.success(data, message, status.HTTP_200_OK)
    
    @staticmethod
    def deleted(message="删除成功"):
        """删除成功响应"""
        return ApiResponse.success(None, message, status.HTTP_200_OK)
    
    @staticmethod
    def not_found(message="资源不存在"):
        """404响应"""
        return ApiResponse.error(message, status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def unauthorized(message="未授权访问"):
        """401响应"""
        return ApiResponse.error(message, status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(message="权限不足"):
        """403响应"""
        return ApiResponse.error(message, status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def validation_error(errors=None, message="参数验证失败"):
        """验证错误响应"""
        return ApiResponse.error(message, status.HTTP_400_BAD_REQUEST, errors)