# KeYan 科研协作平台 - 完整部署指南

## 🎯 部署架构概览

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     用户        │────│     Nginx       │────│   应用服务       │
│                 │    │   (反向代理)    │    │   (Django)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   静态文件       │    │   数据库        │
                       │   (前端)        │    │   (PostgreSQL)  │
                       └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │   监控面板       │    │   缓存         │
                       │   (Grafana)     │    │   (Redis)      │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 快速开始

### 1. 环境准备

#### 系统要求
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- **内存**: 最少 4GB，推荐 8GB+
- **CPU**: 最少 2核，推荐 4核+
- **存储**: 最少 20GB，推荐 50GB+
- **网络**: 公网IP和域名（生产环境）

#### 安装依赖

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git curl wget
```

**CentOS/RHEL:**
```bash
sudo yum update -y
sudo yum install -y docker docker-compose git curl wget
sudo systemctl start docker && sudo systemctl enable docker
```

**Windows:**
```powershell
# 安装 Docker Desktop for Windows
# 安装 Git for Windows
# 安装 Windows Terminal (推荐)
```

### 2. 获取代码

```bash
git clone https://github.com/yourusername/KeYan.git
cd KeYan
```

### 3. 环境配置

#### 3.1 创建环境变量文件

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下关键参数：

```bash
# 数据库配置
POSTGRES_DB=keyan_prod
POSTGRES_USER=keyan_user
POSTGRES_PASSWORD=your_secure_password

# Django配置
SECRET_KEY=your_django_secret_key_here_change_this_in_production_32_chars_min
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# 域名配置
SITE_DOMAIN=yourdomain.com
SITE_URL=https://yourdomain.com

# 邮件配置
EMAIL_HOST=smtp.yourdomain.com
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password
```

#### 3.2 SSL证书配置（生产环境）

**使用 Let's Encrypt:**
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

**证书文件路径：**
- 证书: `/etc/letsencrypt/live/yourdomain.com/fullchain.pem`
- 私钥: `/etc/letsencrypt/live/yourdomain.com/privkey.pem`

## 🏗️ 部署方式

### 方式一：生产环境部署（推荐）

#### 使用一键部署脚本

**Linux/macOS:**
```bash
chmod +x deploy.sh
./deploy.sh start
```

**Windows:**
```powershell
.\deploy.bat start
```

#### 手动部署步骤

1. **构建镜像**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **启动服务**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **数据库迁移**
```bash
docker-compose -f docker-compose.prod.yml run --rm backend python manage.py migrate
```

4. **收集静态文件**
```bash
docker-compose -f docker-compose.prod.yml run --rm backend python manage.py collectstatic --noinput
```

5. **创建超级用户**
```bash
docker-compose -f docker-compose.prod.yml run --rm backend python manage.py createsuperuser
```

### 方式二：开发环境部署

```bash
docker-compose up -d
```

### 方式三：监控环境部署

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

## 📊 服务管理

### 常用操作命令

| 操作 | 命令 |
|------|------|
| 启动服务 | `./deploy.sh start` |
| 停止服务 | `./deploy.sh stop` |
| 重启服务 | `./deploy.sh restart` |
| 更新服务 | `./deploy.sh update` |
| 查看日志 | `./deploy.sh logs` |
| 查看状态 | `./deploy.sh status` |
| 备份数据 | `./deploy.sh backup` |
| 恢复数据 | `./deploy.sh restore` |

### Docker Compose 命令

```bash
# 查看服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f nginx

# 重启单个服务
docker-compose -f docker-compose.prod.yml restart backend

# 进入容器
docker-compose -f docker-compose.prod.yml exec backend bash
```

## 🔍 监控与告警

### 1. 访问监控面板

- **Grafana**: http://yourdomain.com:3000 (admin/admin)
- **Prometheus**: http://yourdomain.com:9090
- **健康检查**: http://yourdomain.com/health/

### 2. 监控指标

#### 系统指标
- CPU 使用率
- 内存使用率
- 磁盘使用率
- 网络流量

#### 应用指标
- HTTP 请求数
- 响应时间
- 错误率
- 数据库连接数

#### 业务指标
- 用户注册数
- 项目创建数
- 文献上传数
- 任务执行数

### 3. 告警规则

#### 系统告警
- CPU 使用率 > 80%
- 内存使用率 > 85%
- 磁盘使用率 > 90%
- 服务不可用

#### 应用告警
- HTTP 错误率 > 5%
- 响应时间 > 2s
- 数据库连接失败

### 4. 设置告警通知

编辑 `monitoring/alertmanager.yml`:

```yaml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@yourdomain.com'
  smtp_auth_username: 'alerts@yourdomain.com'
  smtp_auth_password: 'your_app_password'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
- name: 'web.hook'
  email_configs:
  - to: 'admin@yourdomain.com'
    subject: 'KeYan 告警: {{ .GroupLabels.alertname }}'
    body: |
      {{ range .Alerts }}
      告警: {{ .Annotations.summary }}
      详情: {{ .Annotations.description }}
      时间: {{ .StartsAt.Format "2006-01-02 15:04:05" }}
      {{ end }}
```

## 💾 数据备份与恢复

### 1. 自动备份

#### 使用部署脚本备份
```bash
# 手动备份
./deploy.sh backup

# 设置定时备份
(crontab -l 2>/dev/null; "0 2 * * * /opt/keyan/deploy.sh backup") | crontab -
```

#### 备份内容
- PostgreSQL 数据库
- 用户上传文件
- 配置文件
- 日志文件

### 2. 手动备份

#### 备份数据库
```bash
# 备份数据库
docker-compose -f docker-compose.prod.yml exec db pg_dump -U keyan_user keyan_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# 备份媒体文件
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz /opt/keyan/media/
```

### 3. 数据恢复

```bash
# 恢复数据库
./deploy.sh restore backup_file.sql

# 手动恢复
docker-compose -f docker-compose.prod.yml exec -T db psql -U keyan_user keyan_prod < backup.sql
```

## 🛠️ 故障排除

### 常见问题

#### 1. 服务无法启动

**症状**: 容器启动后立即退出
**排查步骤**:
```bash
# 查看日志
docker-compose -f docker-compose.prod.yml logs backend

# 检查配置
docker-compose -f docker-compose.prod.yml config

# 检查端口占用
netstat -tulnp | grep :80
```

#### 2. 数据库连接失败

**症状**: 应用无法连接数据库
**解决方案**:
```bash
# 检查数据库容器
docker-compose -f docker-compose.prod.yml ps db

# 检查数据库连接
docker-compose -f docker-compose.prod.yml exec db psql -U keyan_user -d keyan_prod

# 重置数据库
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d db
```

#### 3. 静态文件加载失败

**症状**: CSS/JS 文件 404 错误
**解决方案**:
```bash
# 重新收集静态文件
docker-compose -f docker-compose.prod.yml run --rm backend python manage.py collectstatic --noinput

# 检查Nginx配置
nginx -t
```

#### 4. 内存不足

**症状**: 容器频繁重启，系统响应慢
**解决方案**:
```bash
# 查看内存使用
free -h
docker stats

# 优化配置
# 编辑 docker-compose.prod.yml 调整内存限制
```

### 日志分析

#### 查看应用日志
```bash
# 实时查看日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 查看特定时间日志
docker-compose -f docker-compose.prod.yml logs --since 1h backend

# 导出日志
docker-compose -f docker-compose.prod.yml logs backend > app_logs.txt
```

#### 查看系统日志
```bash
# 查看系统日志
journalctl -u docker -f

# 查看Nginx日志
docker-compose -f docker-compose.prod.yml logs nginx
```

## 🔧 性能优化

### 1. 数据库优化

#### PostgreSQL 配置
```sql
# 编辑 docker-compose.prod.yml 中的 PostgreSQL 配置
environment:
  - POSTGRES_DB=keyan_prod
  - POSTGRES_USER=keyan_user
  - POSTGRES_PASSWORD=your_password
  - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
command: >
  postgres
  -c shared_preload_libraries=pg_stat_statements
  -c pg_stat_statements.track=all
  -c max_connections=100
  -c shared_buffers=256MB
  -c effective_cache_size=1GB
  -c maintenance_work_mem=64MB
  -c checkpoint_completion_target=0.9
  -c wal_buffers=16MB
  -c default_statistics_target=100
  -c random_page_cost=1.1
  -c effective_io_concurrency=200
```

### 2. Django 优化

#### 缓存配置
```python
# 在 settings.py 中添加
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# 会话缓存
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

#### 数据库连接池
```python
# 使用连接池
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
    }
}
```

### 3. Nginx 优化

#### 静态文件缓存
```nginx
# 在 nginx.conf 中添加
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Gzip 压缩
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/javascript
    application/xml+rss
    application/json;
```

## 📈 扩展配置

### 1. 水平扩展

#### 使用负载均衡
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  backend:
    deploy:
      replicas: 3
    depends_on:
      - db
      - redis
```

#### 启动多个实例
```bash
docker-compose -f docker-compose.prod.yml -f docker-compose.scale.yml up -d --scale backend=3
```

### 2. CDN 配置

#### CloudFlare 配置
1. 添加域名到 CloudFlare
2. 配置 DNS 记录指向服务器 IP
3. 启用 SSL/TLS 加密
4. 配置缓存规则

### 3. 对象存储

#### AWS S3 配置
```python
# 在 settings.py 中添加
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
```

## 📞 技术支持

### 联系方式
- **邮箱**: support@yourdomain.com
- **QQ群**: 123456789
- **微信**: your_wechat_id

### 文档链接
- [用户手册](docs/user_manual.md)
- [API文档](docs/api.md)
- [常见问题](docs/faq.md)

### 更新日志
- [版本历史](CHANGELOG.md)
- [升级指南](docs/upgrade.md)

## 🎯 下一步计划

1. **自动化测试**: 集成 CI/CD 流程
2. **性能监控**: 添加 APM 工具
3. **日志分析**: 集成 ELK 栈
4. **安全扫描**: 定期安全审计
5. **灾备方案**: 多地域部署

---

**最后更新时间**: 2024-01-01
**文档版本**: v2.0.0