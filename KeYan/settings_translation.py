# 翻译API配置
# 百度翻译API配置
BAIDU_APP_ID = ''  # 请替换为您的百度翻译APP ID
BAIDU_APP_KEY = ''  # 请替换为您的百度翻译APP KEY
BAIDU_SECRET_KEY = ''  # 请替换为您的百度翻译SECRET KEY

# 可选的其他翻译服务配置
# 腾讯翻译API配置
TENCENT_SECRET_ID = ''
TENCENT_SECRET_KEY = ''

# 有道翻译API配置
YOUDAO_APP_KEY = ''
YOUDAO_APP_SECRET = ''

# 缓存配置
TRANSLATION_CACHE_TIMEOUT = 3600  # 翻译结果缓存时间（秒）

# 文件上传配置
FILE_UPLOAD_MAX_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_FILE_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/svg+xml',
]

# PubMed配置
PUBMED_EMAIL = 'research@example.com'  # 用于PubMed API的邮箱
PUBMED_MAX_RESULTS = 100  # 最大搜索结果数量

# 全文获取配置
UNPAYWALL_EMAIL = 'research@example.com'  # 用于获取开放获取文献的邮箱

# 异步任务配置
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# 实时通知配置
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
}