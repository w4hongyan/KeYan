#!/usr/bin/env python3
"""
KeYan 科研协作平台 - 健康检查和监控脚本
用于监控服务状态和性能指标
"""

import os
import sys
import time
import json
import logging
import requests
import psycopg2
import redis
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self):
        self.config = self._load_config()
        self.checks = []
        self.results = []
        
    def _load_config(self) -> Dict:
        """加载配置"""
        return {
            'database_url': os.getenv('DATABASE_URL', 'postgresql://keyan_user:password@localhost:5432/keyan_prod'),
            'redis_url': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
            'base_url': os.getenv('SITE_URL', 'http://localhost'),
            'timeout': 10,
            'retries': 3
        }
    
    def check_database(self) -> Dict:
        """检查数据库连接"""
        try:
            import psycopg2
            conn = psycopg2.connect(self.config['database_url'])
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return {
                'name': 'database',
                'status': 'healthy' if result == (1,) else 'unhealthy',
                'response_time': 0,
                'message': 'Database connection successful' if result == (1,) else 'Database query failed'
            }
        except Exception as e:
            return {
                'name': 'database',
                'status': 'unhealthy',
                'response_time': 0,
                'message': f'Database connection failed: {str(e)}'
            }
    
    def check_redis(self) -> Dict:
        """检查Redis连接"""
        try:
            import redis
            r = redis.from_url(self.config['redis_url'])
            r.ping()
            
            return {
                'name': 'redis',
                'status': 'healthy',
                'response_time': 0,
                'message': 'Redis connection successful'
            }
        except Exception as e:
            return {
                'name': 'redis',
                'status': 'unhealthy',
                'response_time': 0,
                'message': f'Redis connection failed: {str(e)}'
            }
    
    def check_web_service(self) -> Dict:
        """检查Web服务"""
        try:
            import requests
            start_time = time.time()
            response = requests.get(f"{self.config['base_url']}/health/", timeout=self.config['timeout'])
            response_time = time.time() - start_time
            
            return {
                'name': 'web_service',
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': round(response_time, 3),
                'message': f'Web service responded with {response.status_code}',
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'name': 'web_service',
                'status': 'unhealthy',
                'response_time': 0,
                'message': f'Web service check failed: {str(e)}'
            }
    
    def check_disk_space(self) -> Dict:
        """检查磁盘空间"""
        try:
            import shutil
            total, used, free = shutil.disk_usage('/')
            usage_percent = (used / total) * 100
            
            status = 'healthy' if usage_percent < 80 else 'warning' if usage_percent < 90 else 'unhealthy'
            
            return {
                'name': 'disk_space',
                'status': status,
                'response_time': 0,
                'message': f'Disk usage: {usage_percent:.1f}%',
                'usage_percent': round(usage_percent, 1)
            }
        except Exception as e:
            return {
                'name': 'disk_space',
                'status': 'unhealthy',
                'response_time': 0,
                'message': f'Disk space check failed: {str(e)}'
            }
    
    def check_memory_usage(self) -> Dict:
        """检查内存使用"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            usage_percent = memory.percent
            
            status = 'healthy' if usage_percent < 80 else 'warning' if usage_percent < 90 else 'unhealthy'
            
            return {
                'name': 'memory_usage',
                'status': status,
                'response_time': 0,
                'message': f'Memory usage: {usage_percent:.1f}%',
                'usage_percent': round(usage_percent, 1)
            }
        except ImportError:
            return {
                'name': 'memory_usage',
                'status': 'unknown',
                'response_time': 0,
                'message': 'psutil not available'
            }
        except Exception as e:
            return {
                'name': 'memory_usage',
                'status': 'unhealthy',
                'response_time': 0,
                'message': f'Memory usage check failed: {str(e)}'
            }
    
    def run_all_checks(self) -> Dict:
        """运行所有健康检查"""
        checks = [
            self.check_database,
            self.check_redis,
            self.check_web_service,
            self.check_disk_space
        ]
        
        # 如果有 psutil，添加内存检查
        try:
            import psutil
            checks.append(self.check_memory_usage)
        except ImportError:
            pass
        
        results = []
        overall_status = 'healthy'
        
        for check in checks:
            try:
                result = check()
                results.append(result)
                
                if result['status'] == 'unhealthy':
                    overall_status = 'unhealthy'
                elif result['status'] == 'warning' and overall_status == 'healthy':
                    overall_status = 'warning'
                    
            except Exception as e:
                logger.error(f"Check {check.__name__} failed: {str(e)}")
                results.append({
                    'name': check.__name__,
                    'status': 'unhealthy',
                    'response_time': 0,
                    'message': f'Check execution failed: {str(e)}'
                })
                overall_status = 'unhealthy'
        
        return {
            'status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'checks': results
        }
    
    def save_results(self, results: Dict, filename: str = None):
        """保存检查结果"""
        if filename is None:
            filename = f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Health check results saved to {filename}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='KeYan 健康检查工具')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细模式')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    checker = HealthChecker()
    results = checker.run_all_checks()
    
    # 输出结果
    if not args.quiet:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # 保存结果
    if args.output:
        checker.save_results(results, args.output)
    
    # 根据检查结果退出
    if results['status'] == 'healthy':
        sys.exit(0)
    elif results['status'] == 'warning':
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == '__main__':
    main()