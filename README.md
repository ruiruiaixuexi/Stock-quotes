# 股票行情系统

一个基于Django + AKShare + 原生JavaScript的实时股票行情网页系统。

## 🚀 项目特性

- **实时行情**: 获取A股实时股票价格和涨跌信息
- **历史数据**: 查看股票历史价格走势和K线图
- **搜索功能**: 支持按股票代码或名称搜索
- **市场概览**: 显示上证指数、深证成指等市场指标
- **响应式设计**: 支持PC和移动端访问
- **现代化UI**: 美观的界面设计和流畅的用户体验

## 🛠 技术架构

### 后端技术栈
- **Django 4.2+**: Web框架
- **Django REST Framework**: API开发
- **AKShare**: 股票数据获取
- **SQLite**: 数据库（开发环境）
- **Django CORS Headers**: 跨域支持

### 前端技术栈
- **HTML5 + CSS3**: 页面结构和样式
- **原生JavaScript ES6+**: 前端逻辑
- **Chart.js**: 图表展示
- **响应式设计**: 移动端适配

## 📁 项目结构

```
akshare_demo/
├── 📂 stock_project/          # Django项目配置
│   ├── settings.py            # 项目设置
│   ├── urls.py               # 主URL配置
│   ├── wsgi.py               # WSGI配置
│   └── asgi.py               # ASGI配置
├── 📂 stock_app/               # 股票应用
│   ├── models.py             # 数据模型
│   ├── simple_views.py       # 简化API视图
│   ├── mock_service.py        # 模拟数据服务
│   ├── akshare_service.py     # AKShare服务
│   ├── urls.py               # URL路由
│   ├── admin.py              # 管理后台
│   └── apps.py               # 应用配置
├── 📂 frontend/                # 前端静态文件
│   ├── css/
│   │   └── styles.css        # 样式文件
│   └── js/
│       └── app.js            # 前端逻辑
├── 📂 templates/               # Django模板
│   └── index.html            # 主页面
├── 📂 venv/                    # 虚拟环境（已创建）
├── 📄 requirements.txt         # Python依赖
├── 📄 quick_start.py          # 快速启动脚本
├── 📄 PROJECT_STATUS.md       # 项目状态报告
├── 📄 manage.py               # Django管理脚本
├── 📄 db.sqlite3              # SQLite数据库
└── 📄 README.md               # 项目文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- pip
- Git（可选，用于克隆项目）

### 2. 创建虚拟环境

**强烈建议使用虚拟环境来隔离项目依赖！**

#### Windows系统：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 验证虚拟环境（应该显示虚拟环境路径）
where python
```

#### macOS/Linux系统：
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证虚拟环境（应该显示虚拟环境路径）
which python
```

#### 虚拟环境管理：
```bash
# 激活虚拟环境后，命令提示符会显示 (venv)
# 例如：(venv) C:\Users\username\Desktop\akshare_demo>

# 退出虚拟环境
 deactivate

# 重新激活虚拟环境
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```

### 3. 安装依赖

```bash
# 确保虚拟环境已激活（命令提示符显示 (venv)）
# 升级pip到最新版本
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 或者手动安装核心依赖
pip install Django djangorestframework django-cors-headers akshare pandas numpy requests python-dotenv
```

### 3. 数据库迁移

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 4. 启动服务

#### 方法一：使用快速启动脚本（推荐）
```bash
# 确保虚拟环境已激活
python quick_start.py
```

#### 方法二：手动启动
```bash
# 启动开发服务器
python manage.py runserver

# 指定端口启动（可选）
python manage.py runserver 0.0.0.0:8000
```

#### 访问应用
- **前端页面**: http://127.0.0.1:8000/
- **API接口**: http://127.0.0.1:8000/api/
- **管理后台**: http://127.0.0.1:8000/admin/
- **测试端点**: http://127.0.0.1:8000/api/test/

## 📚 API接口

### 核心API接口

- `GET /api/test/` - 测试端点（检查服务状态）
- `GET /api/market/` - 获取市场概览（上证、深证指数）
- `GET /api/stocks/` - 获取股票列表
- `GET /api/stocks/{code}/` - 获取股票详情
- `GET /api/stocks/{code}/realtime/` - 获取实时行情
- `GET /api/stocks/{code}/history/` - 获取历史数据
- `GET /api/search/?q={keyword}` - 搜索股票（支持代码和名称）

### API使用示例

```bash
# 测试服务状态
curl http://127.0.0.1:8000/api/test/

# 获取市场概览
curl http://127.0.0.1:8000/api/market/

# 搜索股票
curl "http://127.0.0.1:8000/api/search/?q=平安"
curl "http://127.0.0.1:8000/api/search/?q=000001"

# 获取股票实时行情
curl http://127.0.0.1:8000/api/stocks/000001/realtime/

# 获取股票历史数据
curl http://127.0.0.1:8000/api/stocks/000001/history/

# 获取股票详情
curl http://127.0.0.1:8000/api/stocks/000001/
```

## 🎯 功能模块

### 1. 市场概览
- 上证指数、深证成指实时数据
- 市场统计信息（上涨、下跌股票数量）
- 自动刷新机制

### 2. 股票搜索
- 支持股票代码和名称搜索
- 实时搜索结果展示
- 搜索历史记录

### 3. 股票详情
- 实时价格和涨跌信息
- 交易数据（开盘、最高、最低、成交量等）
- 价格走势图表
- 历史数据表格

### 4. 数据管理
- 自动缓存机制
- 数据更新策略
- 错误处理和重试

## 🔧 配置说明

### Django设置 (stock_project/settings.py)

```python
# AKShare配置
AKSHARE_TIMEOUT = 30  # 请求超时时间
AKSHARE_RETRY_COUNT = 3  # 重试次数

# CORS配置（开发环境）
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "frontend",
]

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        # ...
    },
]
```

### 数据库配置

默认使用SQLite，生产环境建议使用PostgreSQL：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stock_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 部署指南

### 开发环境部署

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd akshare_demo
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # macOS/Linux: source venv/bin/activate
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

5. **启动服务**
   ```bash
   python quick_start.py  # 推荐方式
   # 或
   python manage.py runserver
   ```

### 生产环境部署

#### 使用Gunicorn + Nginx

1. **安装Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **启动Gunicorn**
   ```bash
   gunicorn stock_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```

3. **配置Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static/ {
           alias /path/to/akshare_demo/frontend/;
       }
   }
   ```

#### 使用Docker（推荐）

```bash
# 构建镜像
docker build -t stock-app .

# 运行容器
docker run -p 8000:8000 stock-app

# 后台运行
docker run -d -p 8000:8000 --name stock-app stock-app
```

## 📊 数据模型

### Stock (股票信息)
- code: 股票代码
- name: 股票名称
- market: 市场（SH/SZ）
- industry: 所属行业

### StockPrice (历史价格)
- stock: 关联股票
- date: 交易日期
- open_price: 开盘价
- high_price: 最高价
- low_price: 最低价
- close_price: 收盘价
- volume: 成交量
- amount: 成交额

### StockRealtime (实时行情)
- stock: 关联股票
- current_price: 当前价格
- change_rate: 涨跌幅
- change_amount: 涨跌金额
- volume: 成交量
- updated_at: 更新时间

## 🔍 故障排除

### 常见问题

1. **虚拟环境问题**
   ```bash
   # 问题：虚拟环境未激活
   # 解决：确保命令提示符显示 (venv)
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. **依赖安装失败**
   ```bash
   # 问题：pip安装失败
   # 解决：升级pip并重试
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **AKShare数据获取失败**
   - ✅ **系统已内置模拟数据服务**
   - 检查网络连接
   - 确认AKShare版本兼容性
   - 查看API限制和频率

4. **前端无法加载数据**
   - 检查CORS配置
   - 确认API端点正确
   - 查看浏览器控制台错误
   - 访问测试端点：http://127.0.0.1:8000/api/test/

5. **数据库连接问题**
   - 检查数据库配置
   - 确认迁移已执行：`python manage.py migrate`
   - 查看数据库权限

6. **端口占用问题**
   ```bash
   # 问题：8000端口被占用
   # 解决：使用其他端口
   python manage.py runserver 8001
   ```

### 调试模式

```python
# 开启调试模式
DEBUG = True

# 查看SQL查询
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📊 项目状态

### ✅ 当前功能状态
- **后端服务**: ✅ 正常运行
- **API接口**: ✅ 全部可用
- **前端界面**: ✅ 响应式设计
- **数据服务**: ✅ 模拟数据 + AKShare回退
- **数据库**: ✅ SQLite已配置
- **虚拟环境**: ✅ 已创建并配置

### 🎯 快速验证
访问以下链接验证系统状态：
- **主页面**: http://127.0.0.1:8000/
- **API测试**: http://127.0.0.1:8000/api/test/
- **市场概览**: http://127.0.0.1:8000/api/market/

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请提交Issue或联系开发者。

---

**⚠️ 重要提示**: 
- 本项目仅用于学习和研究目的
- 股票数据仅供参考，不构成投资建议
- 请确保在虚拟环境中运行项目
- 建议定期更新依赖包版本
