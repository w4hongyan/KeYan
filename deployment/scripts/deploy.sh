#!/bin/bash

# KeYan科研协作平台部署脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_NAME="keyan"
BACKEND_IMAGE="yourusername/keyan-backend"
FRONTEND_IMAGE="yourusername/keyan-frontend"
COMPOSE_FILE="docker-compose.prod.yml"

# 帮助信息
show_help() {
    echo "KeYan部署脚本"
    echo ""
    echo "用法: $0 [COMMAND]"
    echo ""
    echo "命令:"
    echo "  start     启动服务"
    echo "  stop      停止服务"
    echo "  restart   重启服务"
    echo "  update    更新服务"
    echo "  logs      查看日志"
    echo "  backup    备份数据"
    echo "  restore   恢复数据"
    echo "  status    查看状态"
    echo "  init      初始化环境"
    echo "  help      显示帮助"
}

# 检查环境
check_env() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}警告: .env文件不存在，将使用.env.example${NC}"
        cp .env.example .env
    fi
    
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        echo -e "${YELLOW}警告: SSL证书不存在，将使用自签名证书${NC}"
        mkdir -p ssl
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/CN=localhost"
    fi
}

# 启动服务
start_services() {
    echo -e "${GREEN}正在启动服务...${NC}"
    check_env
    docker-compose -f $COMPOSE_FILE up -d
    echo -e "${GREEN}服务启动完成${NC}"
}

# 停止服务
stop_services() {
    echo -e "${YELLOW}正在停止服务...${NC}"
    docker-compose -f $COMPOSE_FILE down
    echo -e "${YELLOW}服务已停止${NC}"
}

# 重启服务
restart_services() {
    echo -e "${GREEN}正在重启服务...${NC}"
    docker-compose -f $COMPOSE_FILE restart
    echo -e "${GREEN}服务重启完成${NC}"
}

# 更新服务
update_services() {
    echo -e "${GREEN}正在更新服务...${NC}"
    docker-compose -f $COMPOSE_FILE pull
    docker-compose -f $COMPOSE_FILE up -d
    echo -e "${GREEN}服务更新完成${NC}"
}

# 查看日志
show_logs() {
    echo -e "${GREEN}查看日志...${NC}"
    if [ -z "$1" ]; then
        docker-compose -f $COMPOSE_FILE logs -f
    else
        docker-compose -f $COMPOSE_FILE logs -f "$1"
    fi
}

# 备份数据
backup_data() {
    echo -e "${GREEN}正在备份数据...${NC}"
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $BACKUP_DIR
    
    # 备份数据库
    docker-compose -f $COMPOSE_FILE exec -T db pg_dump -U ${POSTGRES_USER:-keyan_user} ${POSTGRES_DB:-keyan_db} > $BACKUP_DIR/database.sql
    
    # 备份媒体文件
    cp -r media $BACKUP_DIR/
    
    # 创建压缩包
    tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
    rm -rf $BACKUP_DIR
    
    echo -e "${GREEN}备份完成: $BACKUP_DIR.tar.gz${NC}"
}

# 恢复数据
restore_data() {
    if [ -z "$1" ]; then
        echo -e "${RED}请指定备份文件路径${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}正在恢复数据...${NC}"
    
    # 解压备份
    tar -xzf "$1"
    BACKUP_DIR=$(basename "$1" .tar.gz)
    
    # 恢复数据库
    docker-compose -f $COMPOSE_FILE exec -T db psql -U ${POSTGRES_USER:-keyan_user} -d ${POSTGRES_DB:-keyan_db} < $BACKUP_DIR/database.sql
    
    # 恢复媒体文件
    cp -r $BACKUP_DIR/media/* media/
    
    rm -rf $BACKUP_DIR
    echo -e "${GREEN}数据恢复完成${NC}"
}

# 查看状态
show_status() {
    echo -e "${GREEN}服务状态:${NC}"
    docker-compose -f $COMPOSE_FILE ps
}

# 初始化环境
init_env() {
    echo -e "${GREEN}初始化环境...${NC}"
    
    # 创建必要目录
    mkdir -p media static logs ssl backups
    
    # 设置权限
    chmod 755 media static logs
    
    # 创建.env文件
    if [ ! -f ".env" ]; then
        cp .env.docker .env
        echo -e "${YELLOW}请编辑 .env 文件配置环境变量${NC}"
    fi
    
    # 数据库迁移
    docker-compose -f $COMPOSE_FILE run --rm backend python manage.py migrate
    
    # 创建超级用户
    echo -e "${YELLOW}是否创建超级用户? (y/N):${NC}"
    read -r create_superuser
    if [[ $create_superuser =~ ^[Yy]$ ]]; then
        docker-compose -f $COMPOSE_FILE run --rm backend python manage.py createsuperuser
    fi
    
    echo -e "${GREEN}环境初始化完成${NC}"
}

# 主逻辑
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    update)
        update_services
        ;;
    logs)
        show_logs "$2"
        ;;
    backup)
        backup_data
        ;;
    restore)
        restore_data "$2"
        ;;
    status)
        show_status
        ;;
    init)
        init_env
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac