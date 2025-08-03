# 🔒 安全提交指南

本指南旨在帮助团队成员避免将敏感信息提交到Git仓库。

## 📋 安全提交检查清单

### ✅ 提交前检查
在每次提交前，请确认：

1. **环境变量**：所有API密钥、密码、令牌都存储在环境变量中
2. **配置文件**：敏感配置使用`.env`文件，且`.env`已添加到`.gitignore`
3. **测试数据**：不包含真实用户数据或个人信息
4. **日志文件**：不包含敏感信息的日志文件
5. **数据库**：不包含真实数据库文件或备份

### 🛡️ 敏感信息类型

以下信息**绝对不能**提交到Git：

- **API密钥**：任何服务的API密钥或访问令牌
- **数据库凭据**：数据库连接字符串、用户名、密码
- **JWT密钥**：JWT签名密钥和令牌
- **私钥文件**：RSA、SSH、SSL私钥文件
- **云服务凭证**：AWS、Azure、阿里云、腾讯云等访问密钥
- **个人身份信息**：邮箱、电话号码、身份证号等
- **财务信息**：银行卡号、支付密钥等

### 🛠️ 安全工具

#### 1. 自动安全检查
项目已配置预提交钩子，每次提交前会自动运行：

```bash
# 手动运行安全检查
python scripts/git_security_check.py
```

#### 2. 敏感信息扫描
如果发现潜在敏感信息：

```bash
# 查看具体检测结果
python scripts/git_security_check.py --verbose

# 忽略特定文件（谨慎使用）
python scripts/git_security_check.py --ignore-file path/to/file
```

### 🔧 安全最佳实践

#### 1. 环境变量管理
```bash
# 创建本地环境文件
cp .env.example .env

# 编辑.env文件，添加敏感信息
nano .env
```

#### 2. 配置管理
使用配置文件模板：

```python
# settings.py
import os
from pathlib import Path

# 从环境变量读取敏感信息
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')
API_KEY = os.environ.get('API_KEY')

# 或者从配置文件读取
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()
```

#### 3. 测试数据
使用模拟数据：

```python
# 使用faker生成测试数据
from faker import Faker

fake = Faker()
test_user = {
    'email': fake.email(),
    'name': fake.name(),
    'phone': fake.phone_number()
}
```

### 🚨 紧急情况处理

如果意外提交了敏感信息：

1. **立即撤销提交**：
   ```bash
   git reset --soft HEAD~1
   ```

2. **清理历史记录**（团队协调）：
   ```bash
   # 使用git filter-branch清理历史
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch filename" \
   --prune-empty --tag-name-filter cat -- --all
   ```

3. **更换密钥**：
   - 立即更换所有暴露的API密钥
   - 更新数据库密码
   - 撤销暴露的访问令牌

### 📚 相关文件

- [`.gitignore`](.gitignore) - 忽略规则配置
- [`scripts/git_security_check.py`](scripts/git_security_check.py) - 安全检查脚本
- [`.git/hooks/pre-commit`](.git/hooks/pre-commit) - 预提交钩子

### 🔗 学习资源

- [GitHub敏感信息保护指南](https://docs.github.com/cn/github/authenticating-to-github/keeping-your-account-and-data-secure)
- [OWASP敏感数据处理指南](https://owasp.org/www-project-web-security-testing-guide/)
- [Git最佳实践](https://git-scm.com/book/zh/v2)

### 💡 提示

- 使用`git add -p`逐个添加文件，仔细检查每个变更
- 定期运行安全检查脚本
- 团队成员定期接受安全培训
- 使用代码审查流程，增加安全审查环节

如有疑问，请联系项目维护者或安全团队。