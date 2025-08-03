# 科研综合服务平台 (KeYan)

一个基于Django REST Framework + React构建的综合性科研服务平台，提供文献管理、社区问答、科研合作、科研工具等全方位科研支持。

## 🎯 项目概览

本项目是一个现代化的科研服务平台，为科研人员提供从文献管理到论文发表、从知识分享到科研合作的完整解决方案。

## 📋 已完成功能

### ✅ 核心功能模块

#### 1. 文献管理模块
- **期刊管理**
  - ✅ 期刊CRUD操作
  - ✅ 期刊信息包含：名称、影响因子、中科院分区、JCR分区
  - ✅ 期刊列表API接口

- **文献管理**
  - ✅ 文献CRUD操作
  - ✅ 完整文献元数据：标题、摘要、作者、期刊、发表年份、DOI、PMID等
  - ✅ 文献与期刊关联
  - ✅ 高级搜索和过滤功能

- **用户文献关联**
  - ✅ 用户个人文献收藏
  - ✅ 文献评分系统（1-5星）
  - ✅ 个人备注功能
  - ✅ 收藏标记
  - ✅ 用户专属文献库

#### 2. 社区问答模块
- **问题管理**
  - ✅ 问题CRUD操作
  - ✅ 问题标签系统
  - ✅ 问题投票、收藏、浏览量统计
  - ✅ 问题搜索和过滤

- **回答管理**
  - ✅ 回答CRUD操作
  - ✅ 回答投票系统（赞同/反对）
  - ✅ 最佳回答标记

#### 3. 科研合作模块
- **合作发布**
  - ✅ 合作需求发布（项目合作、论文合作等）
  - ✅ 合作类型分类（项目、论文、数据、技术）
  - ✅ 难度等级标识
  - ✅ 合作状态管理

- **合作申请**
  - ✅ 在线申请参与合作
  - ✅ 申请状态跟踪
  - ✅ 技能标签匹配

#### 4. 用户系统
- **认证系统**
  - ✅ JWT身份认证
  - ✅ 用户注册/登录API
  - ✅ 权限控制（用户只能访问自己的数据）

#### 5. API接口
- **RESTful API设计**
  - ✅ 标准化响应格式
  - ✅ 分页支持
  - ✅ 错误处理机制
  - ✅ Swagger/OpenAPI文档

#### 6. 前端界面
- **React前端**
  - ✅ 现代化React应用
  - ✅ TypeScript支持
  - ✅ Tailwind CSS样式
  - ✅ 响应式设计
  - ✅ 组件化开发

#### 7. 高级功能
- **搜索与过滤**
  - ✅ 全文搜索（标题、作者、关键词）
  - ✅ 按期刊过滤
  - ✅ 按发表年份过滤
  - ✅ 按评分过滤
  - ✅ 按收藏状态过滤
  - ✅ 多字段排序

## 🏗️ 技术架构

### 技术栈

#### 后端
- **框架**: Django 5.0 + Django REST Framework
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）
- **认证**: JWT (djangorestframework-simplejwt)
- **文档**: drf-spectacular (OpenAPI 3.0)
- **过滤**: django-filter
- **测试**: pytest + requests

#### 前端
- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **样式**: Tailwind CSS
- **状态管理**: React Hooks + Context API
- **HTTP客户端**: Axios

### 项目结构
```
KeYan/
├── api/                    # 用户认证系统
├── community/             # 社区问答模块
├── cooperation/           # 科研合作模块
├── literature/            # 文献管理模块
├── frontend/              # React前端应用
├── ky_project/           # Django项目配置
├── templates/            # API文档模板
├── test_complete_api.py   # 完整测试脚本
├── test_journal_api.py    # 期刊API测试
├── test_literature_api.py # 文献API测试
└── README.md             # 项目文档
```

## 🚀 快速开始

### 环境要求
- **后端**: Python 3.8+, Django 5.0+
- **前端**: Node.js 16+, npm
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）

### 后端启动

1. **克隆项目**
```bash
git clone [项目地址]
cd KeYan
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **加载初始数据**
```bash
python manage.py loaddata cooperation/fixtures/initial_skills.json community/fixtures/initial_tags.json
```

6. **创建超级用户**
```bash
python manage.py createsuperuser
```

7. **启动后端开发服务器**
```bash
python manage.py runserver
```

### 前端启动

1. **进入前端目录**
```bash
cd frontend
```

2. **安装前端依赖**
```bash
npm install
```

3. **启动前端开发服务器**
```bash
npm run dev
```

### API测试

运行完整的API测试：
```bash
python test_complete_api.py
```

## 📡 API端点

### 认证系统
- `POST /api/register/` - 用户注册
- `POST /api/login/` - 用户登录
- `POST /api/token/refresh/` - Token刷新

### 文献管理模块
#### 期刊管理
- `GET /api/literature/journals/` - 获取期刊列表
- `POST /api/literature/journals/` - 创建期刊
- `GET /api/literature/journals/{id}/` - 获取期刊详情
- `PUT /api/literature/journals/{id}/` - 更新期刊
- `DELETE /api/literature/journals/{id}/` - 删除期刊

#### 文献管理
- `GET /api/literature/literatures/` - 获取文献列表（支持搜索和过滤）
- `POST /api/literature/literatures/` - 创建文献
- `GET /api/literature/literatures/{id}/` - 获取文献详情
- `PUT /api/literature/literatures/{id}/` - 更新文献
- `DELETE /api/literature/literatures/{id}/` - 删除文献

#### 用户文献关联
- `GET /api/literature/literature-users/` - 获取用户个人文献
- `POST /api/literature/literature-users/` - 创建用户文献关联
- `GET /api/literature/literature-users/{id}/` - 获取用户文献详情
- `PUT /api/literature/literature-users/{id}/` - 更新用户文献信息
- `DELETE /api/literature/literature-users/{id}/` - 删除用户文献关联

### 社区问答模块
#### 问题管理
- `GET /api/community/questions/` - 获取问题列表
- `POST /api/community/questions/` - 创建问题
- `GET /api/community/questions/{id}/` - 获取问题详情
- `PUT /api/community/questions/{id}/` - 更新问题
- `DELETE /api/community/questions/{id}/` - 删除问题
- `POST /api/community/questions/{id}/upvote/` - 赞同问题
- `POST /api/community/questions/{id}/downvote/` - 反对问题
- `POST /api/community/questions/{id}/collect/` - 收藏问题

#### 回答管理
- `GET /api/community/questions/{question_id}/answers/` - 获取问题的回答列表
- `POST /api/community/questions/{question_id}/answers/` - 创建回答
- `GET /api/community/answers/{id}/` - 获取回答详情
- `PUT /api/community/answers/{id}/` - 更新回答
- `DELETE /api/community/answers/{id}/` - 删除回答
- `POST /api/community/answers/{id}/upvote/` - 赞同回答
- `POST /api/community/answers/{id}/downvote/` - 反对回答

#### 标签管理
- `GET /api/community/tags/` - 获取标签列表

### 科研合作模块
#### 合作发布
- `GET /api/cooperation/posts/` - 获取合作帖子列表
- `POST /api/cooperation/posts/` - 发布合作需求
- `GET /api/cooperation/posts/{id}/` - 获取合作详情
- `PUT /api/cooperation/posts/{id}/` - 更新合作信息
- `DELETE /api/cooperation/posts/{id}/` - 删除合作帖子
- `POST /api/cooperation/posts/{id}/apply/` - 申请参与合作

#### 合作申请
- `GET /api/cooperation/posts/{post_id}/applications/` - 获取合作申请列表
- `POST /api/cooperation/posts/{post_id}/applications/` - 提交合作申请
- `GET /api/cooperation/applications/{id}/` - 获取申请详情
- `PUT /api/cooperation/applications/{id}/` - 更新申请状态
- `DELETE /api/cooperation/applications/{id}/` - 删除申请

## 🔍 搜索和过滤功能

### 支持的搜索字段
- **文献搜索**: 标题、作者、关键词
- **期刊搜索**: 期刊名称
- **用户文献**: 文献标题、作者、备注
- **社区问题**: 标题、内容、标签
- **合作需求**: 标题、内容、合作类型

### 支持的过滤条件
- **文献**: 期刊ID、发表年份
- **用户文献**: 期刊、评分、收藏状态
- **社区问题**: 标签、作者、时间范围
- **合作需求**: 合作类型、难度等级、状态、作者

### 支持的排序字段
- **文献**: 发表年份、创建时间、更新时间
- **用户文献**: 创建时间、更新时间、评分
- **社区问题**: 创建时间、更新时间、投票数、浏览量
- **合作需求**: 创建时间、更新时间、申请数量

## 🧪 测试覆盖

### 已验证功能
- ✅ 用户注册和登录
- ✅ 期刊CRUD操作
- ✅ 文献CRUD操作
- ✅ 用户文献关联管理
- ✅ 社区问答功能（问题/回答CRUD、投票）
- ✅ 科研合作功能（发布/申请/管理）
- ✅ 搜索和过滤功能
- ✅ 权限控制
- ✅ 数据验证
- ✅ 错误处理
- ✅ API文档自动生成

## 🚧 待开发功能

### 前端界面开发
- ✅ 首页设计和响应式布局
- ✅ 用户注册/登录页面
- ✅ 文献管理界面（列表/详情/编辑）
- ✅ 社区问答界面（问题列表/详情/提问）
- ✅ 科研合作界面（合作列表/详情/发布）
- ✅ 个人中心界面
- ✅ 搜索功能界面
- ✅ 用户个人资料管理

### 高级功能
- ✅ PubMed API集成
- ✅ 文献翻译服务
- ✅ 科研绘图工具
- ✅ 统计分析模块
- ✅ 论文查重服务
- ✅ 邮件通知系统
- ✅ 文件上传功能
- ✅ 富文本编辑器
- ✅ 数据可视化图表

### 性能优化
- ✅ 数据库索引优化
- ✅ 缓存机制
- ✅ CDN集成
- ✅ 图片压缩
- ✅ 前端代码分割

### 部署配置
- ✅ Docker容器化
- ✅ CI/CD流水线
- ✅ 生产环境配置
- ✅ 监控日志系统
- ✅ 期刊影响因子查询

### 管理后台
- [ ] 用户管理系统
- [ ] 订单管理
- [ ] 内容管理
- [ ] 数据统计

## 📊 数据库设计

### 主要模型

#### Journal (期刊)
- name: 期刊名称
- impact_factor: 影响因子
- cas_partition: 中科院分区
- jcr_partition: JCR分区

#### Literature (文献)
- title: 文献标题
- abstract: 文献摘要
- authors: 作者信息
- journal: 关联期刊
- pub_year: 发表年份
- doi: DOI标识符
- pmid: PMID标识符
- keywords: 关键词

#### LiteratureUser (用户文献关联)
- user: 关联用户
- literature: 关联文献
- rating: 评分(1-5星)
- notes: 个人备注
- is_favorite: 收藏标记

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱：[your-email@example.com]
- GitHub Issues

---

**项目状态**: 核心功能已完成，前端界面开发完成95%，持续优化中 🚀