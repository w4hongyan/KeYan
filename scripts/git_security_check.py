#!/usr/bin/env python3
"""
Git安全提交检查脚本
用于检测和防止敏感信息被意外提交到Git仓库
"""

import os
import re
import sys
import json
from pathlib import Path

class GitSecurityChecker:
    def __init__(self):
        self.sensitive_patterns = [
            # 高优先级：真实的API密钥格式
            (r'(?i)sk-[a-zA-Z0-9]{32,}', 'OpenAI API Key'),
            (r'(?i)AKIA[0-9A-Z]{16}', 'AWS Access Key'),
            (r'(?i)[0-9a-zA-Z/+]{40}(?=[^a-zA-Z0-9]|$)', 'AWS Secret Key'),
            
            # 数据库连接字符串（真实格式）
            (r'(?i)(mongodb|mysql|postgresql|postgres)://[^:\s]+:[^@\s]+@[^/\s]+/[^\s\'"]*', 'Database URL with Password'),
            
            # JWT令牌（完整格式）
            (r'(?i)eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}', 'JWT Token'),
            
            # 私钥文件（排除脚本自身）
            (r'(?<!# Example: )-----BEGIN PRIVATE KEY-----', 'Private Key'),
            (r'(?<!# Example: )-----BEGIN RSA PRIVATE KEY-----', 'RSA Private Key'),
            (r'(?<!# Example: )-----BEGIN OPENSSH PRIVATE KEY-----', 'SSH Private Key'),
            (r'(?<!# Example: )-----BEGIN CERTIFICATE-----', 'SSL Certificate'),
            
            # 强密码（排除代码中的变量名和字典键）
            (r'(?i)(password|passwd|pwd|secret|token|key)\s*[:=]\s*["\']?([a-zA-Z0-9@#$%^&+=]{12,})["\']?(?![a-zA-Z])(?<!key:)', 'Strong Password'),
            
            # 云服务密钥
            (r'(?i)gcp-[a-zA-Z0-9]{12,}', 'GCP Service Account Key'),
            (r'(?i)[a-z0-9]{32,44}(?=[^a-z0-9]|$)(?<![A-Z])', 'Generic API Key'),
        ]
        
        self.ignore_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env',
            'dist', 'build', '.pytest_cache', '.coverage', '.mypy_cache',
            'logs', 'tmp', 'temp', '.docker', '.idea', '.vscode'
        }
        
        self.ignore_extensions = {
            '.pyc', '.pyo', '.pyd', '.so', '.egg', '.egg-info', '.log',
            '.sqlite', '.sqlite3', '.db', '.bak', '.tmp', '.temp',
            '.swp', '.swo', '~', '.DS_Store'
        }

    def scan_file(self, file_path):
        """扫描单个文件中的敏感信息"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern, issue_type in self.sensitive_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    # 排除一些常见的假阳性
                    if self._is_false_positive(match.group(), file_path):
                        continue
                        
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append({
                        'file': str(file_path),
                        'line': line_num,
                        'type': issue_type,
                        'match': match.group()[:50] + '...' if len(match.group()) > 50 else match.group()
                    })
                    
        except (IOError, OSError):
            pass
            
        return issues

    def _is_false_positive(self, match, file_path):
        """检查是否为假阳性"""
        file_path_str = str(file_path).lower()
        match_lower = match.lower()
        
        # 忽略静态文件和第三方库
        if any(skip in file_path_str for skip in [
            'staticfiles/', 'node_modules/', '.git/', '__pycache__/', 
            '.venv/', 'venv/', 'env/', 'dist/', 'build/',
            'rest_framework/', 'jquery', 'bootstrap', 'coreapi'
        ]):
            return True
            
        # 忽略示例/模板/测试文件
        if any(x in file_path_str for x in [
            'example', 'template', 'sample', 'test', 'mock', 'fixture', 'dummy'
        ]):
            return True
            
        # 忽略注释中的内容
        if any(match.strip().startswith(prefix) for prefix in ['#', '//', '/*', '*', '<!--']):
            return True
            
        # 忽略占位符和示例值
        placeholders = [
            'your_api_key', 'api_key_here', 'placeholder', 'example', 
            'changeme', 'password123', 'secret123', 'test123', 'demo',
            'fake_', 'mock_', 'sample_', 'example_', 'change_this',
            'change_this_password', 'change_this_secret_key', 'your_',
            'your_secure_db_password', 'your_openai_api_key'
        ]
        if any(placeholder in match_lower for placeholder in placeholders):
            return True
            
        # 忽略变量名和函数参数
        if any(keyword in match_lower for keyword in [
            'function', 'def ', 'class ', 'var ', 'let ', 'const ', 
            'password_field', 'password_input', 'get_password'
        ]):
            return True
            
        # 忽略HTML/CSS/JS中的常见属性
        if any(attr in match_lower for attr in [
            'password:true', 'type="password"', 'password:', 'password: !0',
            'password=!0', 'password:', 'username:'
        ]):
            return True
            
        return False

    def should_ignore_file(self, file_path):
        """判断是否应该忽略该文件"""
        path = Path(file_path)
        
        # 忽略目录
        if any(ignore_dir in str(path).split(os.sep) for ignore_dir in self.ignore_dirs):
            return True
            
        # 忽略扩展名
        if path.suffix.lower() in self.ignore_extensions:
            return True
            
        # 忽略静态文件和第三方库
        if any(skip in str(path) for skip in [
            'staticfiles/', 'node_modules/', '.git/', 
            '__pycache__/', '.venv/', 'venv/'
        ]):
            return True
            
        return False

    def scan_directory(self, directory='.'):
        """扫描整个目录"""
        issues = []
        
        # 完全忽略的目录和文件
        skip_dirs = {'staticfiles', 'node_modules', '.git', '__pycache__', 
                    '.venv', 'venv', 'env', 'dist', 'build', '.pytest_cache', 'frontend'}
        skip_files = {'git_security_check.py', 'package-lock.json', 'package.json'}  # 跳过自身和前端文件
        skip_extensions = {'.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.json'}
        
        for root, dirs, files in os.walk(directory):
            # 过滤掉应该忽略的目录
            dirs[:] = [d for d in dirs if d not in skip_dirs and not self.should_ignore_file(os.path.join(root, d))]
            
            # 跳过静态文件目录和脚本自身
            if any(skip_dir in root for skip_dir in skip_dirs):
                continue
                
            for file in files:
                if file in skip_files:
                    continue
                    
                file_path = os.path.join(root, file)
                if Path(file_path).suffix.lower() in skip_extensions:
                    continue
                    
                if not self.should_ignore_file(file_path):
                    file_issues = self.scan_file(file_path)
                    issues.extend(file_issues)
        
        return issues

    def generate_report(self, issues):
        """生成扫描报告"""
        if not issues:
            print("✅ 未发现敏感信息")
            return True
            
        print("⚠️  发现潜在敏感信息：")
        print("=" * 60)
        
        for issue in issues:
            print(f"📁 文件: {issue['file']}")
            print(f"📍 行号: {issue['line']}")
            print(f"🔍 类型: {issue['type']}")
            print(f"📝 内容: {issue['match']}")
            print("-" * 60)
            
        return False

def main():
    """主函数"""
    print("🔒 Git安全提交检查工具")
    print("正在扫描项目中的敏感信息...")
    
    checker = GitSecurityChecker()
    issues = checker.scan_directory('.')
    
    success = checker.generate_report(issues)
    
    if not success:
        print("\n❌ 发现敏感信息，建议：")
        print("1. 将敏感信息移至环境变量或配置文件")
        print("2. 使用占位符替换敏感信息")
        print("3. 将敏感文件添加到.gitignore")
        sys.exit(1)
    else:
        print("\n✅ 安全检查通过，可以安全提交！")

if __name__ == "__main__":
    main()