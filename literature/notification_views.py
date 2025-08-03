from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .notification_service import NotificationService, NotificationManager
from .utils import ApiResponse

class NotificationListView(APIView):
    """通知列表API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """获取用户通知列表"""
        user_id = request.query_params.get('user_id', 'default_user')
        limit = int(request.query_params.get('limit', 20))
        
        try:
            service = NotificationService()
            notifications = service.get_notifications(user_id, limit)
            
            return Response(
                ApiResponse.success({
                    'notifications': notifications,
                    'total': len(notifications)
                }),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"获取通知列表失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NotificationReadView(APIView):
    """通知已读API"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """标记通知为已读"""
        user_id = request.data.get('user_id', 'default_user')
        notification_id = request.data.get('notification_id')
        
        if not notification_id:
            return Response(
                ApiResponse.error("未提供通知ID"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = NotificationService()
            service.mark_as_read(user_id, notification_id)
            
            return Response(
                ApiResponse.success(None, "通知已标记为已读"),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"标记通知失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NotificationUnreadCountView(APIView):
    """未读通知数量API"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """获取未读通知数量"""
        user_id = request.query_params.get('user_id', 'default_user')
        
        try:
            service = NotificationService()
            count = service.get_unread_count(user_id)
            
            return Response(
                ApiResponse.success({'count': count}),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"获取未读数量失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NotificationTestView(APIView):
    """通知测试API"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """发送测试通知"""
        user_id = request.data.get('user_id', 'default_user')
        message_type = request.data.get('type', 'system_message')
        message = request.data.get('message', '测试通知')
        
        try:
            manager = NotificationManager()
            
            if message_type == 'literature_imported':
                manager.notify_literature_imported(user_id, 10)
            elif message_type == 'translation_complete':
                manager.notify_translation_complete(user_id, 123, '中文')
            elif message_type == 'pubmed_search_complete':
                manager.notify_pubmed_search_complete(user_id, 'cancer research', 25)
            elif message_type == 'file_upload_complete':
                manager.notify_file_upload_complete(user_id, 'test.pdf')
            elif message_type == 'error':
                manager.notify_error(user_id, '测试错误消息', 'test_operation')
            else:
                manager.notify_system_message(user_id, message)
            
            return Response(
                ApiResponse.success(None, "测试通知已发送"),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                ApiResponse.error(f"发送测试通知失败: {str(e)}"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )