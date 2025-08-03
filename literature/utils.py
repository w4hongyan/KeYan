class ApiResponse:
    """标准化API响应格式"""
    
    @staticmethod
    def success(data=None, message="操作成功"):
        """成功响应"""
        return {
            'success': True,
            'message': message,
            'data': data
        }
    
    @staticmethod
    def error(message="操作失败", code=None):
        """错误响应"""
        response = {
            'success': False,
            'message': message,
            'data': None
        }
        if code:
            response['code'] = code
        return response
    
    @staticmethod
    def paginated(data, total, page, page_size, message="获取成功"):
        """分页响应"""
        return {
            'success': True,
            'message': message,
            'data': {
                'results': data,
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        }