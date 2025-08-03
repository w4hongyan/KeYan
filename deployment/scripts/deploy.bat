@echo off
REM KeYan科研协作平台Windows部署脚本

setlocal enabledelayedexpansion

REM 颜色设置
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "NC=[0m"

REM 配置变量
set "PROJECT_NAME=keyan"
set "COMPOSE_FILE=docker-compose.prod.yml"

:help
if "%1"=="help" goto show_help
if "%1"=="--help" goto show_help
if "%1"=="-h" goto show_help
goto main

:show_help
echo KeYan部署脚本
echo.
echo 用法: %0 [COMMAND]
echo.
echo 命令:
echo   start     启动服务
echo   stop      停止服务
echo   restart   重启服务
echo   update    更新服务
echo   logs      查看日志
echo   backup    备份数据
echo   status    查看状态
echo   init      初始化环境
echo   help      显示帮助
echo.
goto :eof

:check_env
if not exist ".env" (
    echo %YELLOW%警告: .env文件不存在，将使用.env.docker%NC%
    copy .env.docker .env
)

if not exist "ssl\cert.pem" (
    echo %YELLOW%警告: SSL证书不存在，生产环境需要配置SSL证书%NC%
    mkdir ssl 2>nul
)
goto :eof

:start
echo %GREEN%正在启动服务...%NC%
call :check_env
docker-compose -f %COMPOSE_FILE% up -d
if %errorlevel% neq 0 (
    echo %RED%启动失败，请检查Docker环境%NC%
    exit /b 1
)
echo %GREEN%服务启动完成%NC%
goto :eof

:stop
echo %YELLOW%正在停止服务...%NC%
docker-compose -f %COMPOSE_FILE% down
if %errorlevel% neq 0 (
    echo %RED%停止失败%NC%
    exit /b 1
)
echo %YELLOW%服务已停止%NC%
goto :eof

:restart
echo %GREEN%正在重启服务...%NC%
docker-compose -f %COMPOSE_FILE% restart
if %errorlevel% neq 0 (
    echo %RED%重启失败%NC%
    exit /b 1
)
echo %GREEN%服务重启完成%NC%
goto :eof

:update
echo %GREEN%正在更新服务...%NC%
docker-compose -f %COMPOSE_FILE% pull
docker-compose -f %COMPOSE_FILE% up -d
if %errorlevel% neq 0 (
    echo %RED%更新失败%NC%
    exit /b 1
)
echo %GREEN%服务更新完成%NC%
goto :eof

:logs
echo %GREEN%查看日志...%NC%
if "%2"=="" (
    docker-compose -f %COMPOSE_FILE% logs -f
) else (
    docker-compose -f %COMPOSE_FILE% logs -f %2
)
goto :eof

:backup
echo %GREEN%正在备份数据...%NC%
set "BACKUP_DIR=backups\%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
mkdir "%BACKUP_DIR%" 2>nul

REM 备份数据库
docker-compose -f %COMPOSE_FILE% exec -T db pg_dump -U %POSTGRES_USER% %POSTGRES_DB% > "%BACKUP_DIR%\database.sql"

REM 备份媒体文件
xcopy media "%BACKUP_DIR%\media\" /E /I /Q

REM 创建压缩包
powershell -Command "Compress-Archive -Path '%BACKUP_DIR%' -DestinationPath '%BACKUP_DIR%.zip'"
rd /s /q "%BACKUP_DIR%"

echo %GREEN%备份完成: %BACKUP_DIR%.zip%NC%
goto :eof

:status
echo %GREEN%服务状态:%NC%
docker-compose -f %COMPOSE_FILE% ps
goto :eof

:init
echo %GREEN%初始化环境...%NC%

REM 创建必要目录
mkdir media static logs ssl backups 2>nul

REM 创建.env文件
if not exist ".env" (
    copy .env.docker .env
    echo %YELLOW%请编辑 .env 文件配置环境变量%NC%
)

REM 数据库迁移
docker-compose -f %COMPOSE_FILE% run --rm backend python manage.py migrate
if %errorlevel% neq 0 (
    echo %RED%数据库迁移失败%NC%
    exit /b 1
)

echo %GREEN%环境初始化完成%NC%
goto :eof

:main
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="update" goto update
if "%1"=="logs" goto logs
if "%1"=="backup" goto backup
if "%1"=="status" goto status
if "%1"=="init" goto init
if "%1"=="" goto show_help

echo %RED%未知命令: %1%NC%
call :show_help
goto :eof