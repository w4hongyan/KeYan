# KeYan 部署配置目录

此目录包含所有与部署相关的配置文件和脚本。

## 目录结构

```
deployment/
├── README.md              # 本说明文档
├── .env.example           # 环境变量模板
├── docker/                # Docker配置文件
│   ├── docker-compose/
│   │   ├── docker-compose.yml           # 开发环境
│   │   ├── docker-compose.prod.yml      # 生产环境
│   │   └── docker-compose.monitoring.yml  # 监控环境
│   ├── Dockerfile/          # Dockerfile文件
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── Dockerfile.healthcheck
│   └── nginx/             # Nginx配置
│       ├── nginx.conf       # 开发环境配置
│       └── nginx.prod.conf  # 生产环境配置
├── scripts/               # 部署脚本
│   ├── deploy.sh          # Linux/macOS部署脚本
│   ├── deploy.bat         # Windows部署脚本
│   └── health_check.py    # 健康检查脚本
├── monitoring/            # 监控配置
│   ├── prometheus.yml     # Prometheus配置
│   ├── alertmanager.yml   # 告警配置
│   └── grafana/           # Grafana仪表板配置
├── ssl/                   # SSL证书目录
├── backups/               # 备份文件目录
└── docs/                  # 部署文档
    └── DEPLOYMENT.md      # 完整部署指南
```

## 快速开始

1. **开发环境**:
   ```bash
   docker-compose -f deployment/docker-compose/docker-compose.yml up -d
   ```

2. **生产环境**:
   ```bash
   cd deployment
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh start
   ```

3. **监控环境**:
   ```bash
   docker-compose -f deployment/docker-compose/docker-compose.monitoring.yml up -d
   ```

## 配置文件说明

### Docker Compose文件
- **docker-compose.yml**: 开发环境，包含基本服务
- **docker-compose.prod.yml**: 生产环境，包含完整服务栈和优化配置
- **docker-compose.monitoring.yml**: 监控环境，包含Prometheus、Grafana等

### Nginx配置
- **nginx.conf**: 开发环境配置，简单反向代理
- **nginx.prod.conf**: 生产环境配置，包含HTTPS、缓存、安全头等

### 环境变量
- **.env.example**: 环境变量模板
- **.env.docker**: Docker专用环境变量

### 部署脚本
- **deploy.sh**: Linux/macOS一键部署脚本
- **deploy.bat**: Windows一键部署脚本
- **health_check.py**: 服务健康检查脚本