# KeYan 科研协作平台 - 项目结构说明

## 📁 根目录结构

```
KeYan/
├── api/                          # Django后端API
├── frontend/                     # Vue3前端项目
├── deployment/                   # 部署配置目录（新整理）
├── media/                        # 媒体文件
├── staticfiles/                  # 静态文件收集目录
├── manage.py                    # Django管理脚本
├── requirements.txt              # Python依赖
└── PROJECT_STRUCTURE.md        # 本文件
```

## 🚀 deployment目录结构（新整理）

```
deployment/
├── README.md                   # 部署目录说明
├── .env.example               # 环境变量模板
├── docker/                     # Docker相关配置
│   ├── docker-compose/        # Docker Compose文件
│   │   ├── docker-compose.yml         # 开发环境
│   │   ├── docker-compose.prod.yml    # 生产环境
│   │   └── docker-compose.monitoring.yml # 监控环境
│   ├── dockerfile/           # Dockerfile文件
│   │   └── Dockerfile.healthcheck     # 健康检查容器
│   └── nginx/                # Nginx配置
│       ├── nginx.conf                 # 开发配置
│       └── nginx.prod.conf            # 生产配置
├── scripts/                    # 部署脚本
│   ├── deploy.sh              # Linux/macOS部署脚本
│   ├── deploy.bat             # Windows部署脚本
│   └── health_check.py        # 健康检查脚本
├── monitoring/               # 监控配置
│   └── prometheus.yml         # Prometheus配置
├── docs/                     # 部署文档
│   └── DEPLOYMENT.md          # 详细部署指南
├── ssl/                      # SSL证书目录（空）
└── backups/                  # 备份文件目录（空）
```

## 🎯 快速开始

### 开发环境
```bash
cd deployment
docker-compose -f docker/docker-compose/docker-compose.yml up -d
```

### 生产环境
```bash
cd deployment
./scripts/deploy.sh  # Linux/macOS
# 或
.\scripts\deploy.bat  # Windows
```

### 监控环境
```bash
cd deployment
docker-compose -f docker/docker-compose/docker-compose.monitoring.yml up -d
```

## 📋 配置文件说明

| 文件 | 用途 |
|------|------|
| `.env.example` | 环境变量模板 |
| `docker-compose*.yml` | 不同环境的容器编排 |
| `nginx*.conf` | Nginx反向代理配置 |
| `prometheus.yml` | 监控目标配置 |
| `health_check.py` | 服务健康检查 |
| `deploy.sh/.bat` | 一键部署脚本 |

## 🔄 迁移说明

所有部署相关文件已从根目录迁移至 `deployment/` 目录，保持根目录整洁，便于项目管理。