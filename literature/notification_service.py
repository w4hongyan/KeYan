import json
from typing import Dict, List, Optional
from datetime import datetime
import redis

class NotificationService:
    """实时通知服务"""
    
    def __init__(self):
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_client.ping()
        except redis.ConnectionError:
            # 如果Redis不可用，使用内存存储
            self.redis_client = None
            self._memory_storage = {}
        self.notification_channel = 'notifications'
    
    def send_notification(self, user_id: str, notification_type: str, message: str, data: Dict = None):
        """发送通知"""
        notification = {
            'id': f"{user_id}_{datetime.now().timestamp()}",
            'user_id': user_id,
            'type': notification_type,
            'message': message,
            'data': data or {},
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        if self.redis_client:
            # 存储到Redis
            key = f"notifications:{user_id}"
            self.redis_client.lpush(key, json.dumps(notification))
            self.redis_client.ltrim(key, 0, 99)  # 只保留最近100条通知
        else:
            # 使用内存存储
            key = f"notifications:{user_id}"
            if key not in self._memory_storage:
                self._memory_storage[key] = []
            self._memory_storage[key].insert(0, notification)
            self._memory_storage[key] = self._memory_storage[key][:100]
        
        return notification
    
    def get_notifications(self, user_id: str, limit: int = 20) -> List[Dict]:
        """获取用户通知"""
        if self.redis_client:
            key = f"notifications:{user_id}"
            notifications = self.redis_client.lrange(key, 0, limit - 1)
            return [json.loads(n) for n in notifications]
        else:
            # 从内存获取
            key = f"notifications:{user_id}"
            notifications = self._memory_storage.get(key, [])
            return notifications[:limit]
    
    def mark_as_read(self, user_id: str, notification_id: str):
        """标记通知为已读"""
        if self.redis_client:
            key = f"notifications:{user_id}"
            notifications = self.redis_client.lrange(key, 0, -1)
            
            for i, notification_str in enumerate(notifications):
                notification = json.loads(notification_str)
                if notification['id'] == notification_id:
                    notification['read'] = True
                    self.redis_client.lset(key, i, json.dumps(notification))
                    break
        else:
            # 标记内存中的通知为已读
            key = f"notifications:{user_id}"
            if key in self._memory_storage:
                for notification in self._memory_storage[key]:
                    if notification['id'] == notification_id:
                        notification['read'] = True
                        break
    
    def get_unread_count(self, user_id: str) -> int:
        """获取未读通知数量"""
        notifications = self.get_notifications(user_id, 100)
        return sum(1 for n in notifications if not n.get('read', False))

class NotificationManager:
    """通知管理器"""
    
    def __init__(self):
        self.service = NotificationService()
    
    def notify_literature_imported(self, user_id: str, count: int):
        """通知文献导入完成"""
        return self.service.send_notification(
            user_id,
            'literature_imported',
            f'成功导入 {count} 篇文献',
            {'count': count}
        )
    
    def notify_translation_complete(self, user_id: str, literature_id: int, language: str):
        """通知翻译完成"""
        return self.service.send_notification(
            user_id,
            'translation_complete',
            f'文献翻译完成 ({language})',
            {'literature_id': literature_id, 'language': language}
        )
    
    def notify_pubmed_search_complete(self, user_id: str, query: str, count: int):
        """通知PubMed搜索完成"""
        return self.service.send_notification(
            user_id,
            'pubmed_search_complete',
            f'PubMed搜索完成: 找到 {count} 篇文献',
            {'query': query, 'count': count}
        )
    
    def notify_file_upload_complete(self, user_id: str, filename: str):
        """通知文件上传完成"""
        return self.service.send_notification(
            user_id,
            'file_upload_complete',
            f'文件上传成功: {filename}',
            {'filename': filename}
        )
    
    def notify_error(self, user_id: str, error_message: str, operation: str):
        """通知错误"""
        return self.service.send_notification(
            user_id,
            'error',
            f'操作失败: {error_message}',
            {'operation': operation, 'error': error_message}
        )
    
    def notify_system_message(self, user_id: str, message: str):
        """通知系统消息"""
        return self.service.send_notification(
            user_id,
            'system_message',
            message,
            {}
        )

# 创建全局实例
notification_service = NotificationService()
notification_manager = NotificationManager()