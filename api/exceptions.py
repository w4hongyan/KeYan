from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.views import exception_handler
from .utils import ApiResponse

def custom_exception_handler(exc, context):
    # 调用DRF默认的异常处理器获取标准错误响应
    response = exception_handler(exc, context)
    
    # 如果DRF无法处理该异常，返回None，我们保持原样
    if response is None:
        return response
    
    # 统一处理验证错误
    if hasattr(exc, 'detail'):
        # 处理序列化器验证错误
        if isinstance(exc.detail, dict):
            return ApiResponse.error(
                message="参数验证失败",
                code=response.status_code,
                errors=exc.detail
            )
        # 处理其他DRF异常
        else:
            return ApiResponse.error(
                message=str(exc.detail),
                code=response.status_code
            )
    
    # 返回原始响应（不应该到达这里）
    return response