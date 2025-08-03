#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KeYan.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
from api.models import Literature, Question, Collaboration, UserProfile
import logging

logger = logging.getLogger(__name__)

def create_indexes():
    """创建数据库索引优化"""
    
    with connection.cursor() as cursor:
        logger.info("开始创建数据库索引...")
        
        # Literature表的索引
        indexes = [
            # 文献标题索引
            "CREATE INDEX IF NOT EXISTS idx_literature_title ON api_literature (title);",
            
            # 作者索引
            "CREATE INDEX IF NOT EXISTS idx_literature_author ON api_literature (author);",
            
            # 创建时间索引
            "CREATE INDEX IF NOT EXISTS idx_literature_created_at ON api_literature (created_at);",
            
            # 用户ID和创建时间复合索引
            "CREATE INDEX IF NOT EXISTS idx_literature_user_created ON api_literature (user_id, created_at);",
            
            # 研究领域索引
            "CREATE INDEX IF NOT EXISTS idx_literature_field ON api_literature (field);",
            
            # 全文搜索索引（PostgreSQL）
            "CREATE INDEX IF NOT EXISTS idx_literature_search ON api_literature USING gin(to_tsvector('english', title || ' ' || abstract));",
            
            # Question表的索引
            "CREATE INDEX IF NOT EXISTS idx_question_user ON api_question (user_id);",
            "CREATE INDEX IF NOT EXISTS idx_question_created ON api_question (created_at);",
            "CREATE INDEX IF NOT EXISTS idx_question_status ON api_question (status);",
            
            # Collaboration表的索引
            "CREATE INDEX IF NOT EXISTS idx_collaboration_user ON api_collaboration (user_id);",
            "CREATE INDEX IF NOT EXISTS idx_collaboration_created ON api_collaboration (created_at);",
            "CREATE INDEX IF NOT EXISTS idx_collaboration_status ON api_collaboration (status);",
            
            # UserProfile表的索引
            "CREATE INDEX IF NOT EXISTS idx_userprofile_user ON api_userprofile (user_id);",
            "CREATE INDEX IF NOT EXISTS idx_userprofile_research_field ON api_userprofile (research_field);",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
                logger.info(f"创建索引成功: {index_sql}")
            except Exception as e:
                logger.error(f"创建索引失败: {index_sql}, 错误: {str(e)}")
        
        logger.info("数据库索引创建完成")

def analyze_tables():
    """分析表统计信息"""
    with connection.cursor() as cursor:
        tables = [
            'api_literature',
            'api_question', 
            'api_collaboration',
            'api_userprofile',
            'auth_user'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"ANALYZE {table};")
                logger.info(f"分析表 {table} 完成")
            except Exception as e:
                logger.error(f"分析表 {table} 失败: {str(e)}")

def check_index_usage():
    """检查索引使用情况"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT schemaname, tablename, attname, n_distinct, correlation
            FROM pg_stats
            WHERE schemaname = 'public'
            AND tablename IN ('api_literature', 'api_question', 'api_collaboration', 'api_userprofile')
            ORDER BY tablename, attname;
        """)
        
        stats = cursor.fetchall()
        logger.info("表统计信息:")
        for row in stats:
            logger.info(f"表: {row[1]}, 列: {row[2]}, 唯一值: {row[3]}, 相关性: {row[4]}")

def main():
    """主函数"""
    logger.info("开始数据库优化...")
    
    # 创建索引
    create_indexes()
    
    # 分析表
    analyze_tables()
    
    # 检查统计信息
    check_index_usage()
    
    logger.info("数据库优化完成")

if __name__ == "__main__":
    main()