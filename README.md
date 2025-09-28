# Stock-quotes# 股票行情系统

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
├── stock_project/          # Django项目配置
│   ├── settings.py        # 项目设置
│   ├── urls.py           # 主URL配置
│   ├── wsgi.py           # WSGI配置
│   └── asgi.py           # ASGI配置
├── stock_app/             # 股票应用
│   ├── models.py         # 数据模型
│   ├── views.py          # API视图
│   ├── serializers.py    # 序列化器
│   ├── urls.py           # URL路由
│   ├── admin.py          # 管理后台
│   └── akshare_service.py # AKShare服务
├── frontend/              # 前端静态文件
│   ├── css/
│   │   └── styles.css    # 样式文件
│   └── js/
│       └── app.js        # 前端逻辑
├── templates/             # Django模板
│   └── index.html        # 主页面
├── requirements.txt       # Python依赖
├── manage.py             # Django管理脚本
└── README.md             # 项目文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- pip

### 2. 安装依赖

```bash
# 安装Python依赖包
pip install Django djangorestframework django-cors-headers akshare pandas

# 或者使用requirements.txt
pip install -r requirements.txt
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

```bash
# 启动开发服务器
python manage.py runserver

# 访问应用
# 前端页面: http://127.0.0.1:8000/
# API文档: http://127.0.0.1:8000/api/
# 管理后台: http://127.0.0.1:8000/admin/
```

## 📚 API接口

### 股票相关接口

- `GET /api/stocks/` - 获取股票列表
- `GET /api/stocks/{code}/` - 获取股票详情
- `GET /api/stocks/{code}/realtime/` - 获取实时行情
- `GET /api/stocks/{code}/history/` - 获取历史数据

### 搜索和市场接口

- `GET /api/search/?q={keyword}` - 搜索股票
- `GET /api/market/` - 获取市场概览
- `GET /api/list/` - 获取股票列表（分页）

### 请求参数示例

```bash
# 获取股票历史数据
GET /api/stocks/000001/history/?start_date=2024-01-01&end_date=2024-01-31&period=daily

# 搜索股票
GET /api/search/?q=平安银行

# 分页获取股票列表
GET /api/list/?page=1&page_size=20
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

### Django设置 (settings.py)

```python
# AKShare配置
AKSHARE_TIMEOUT = 30  # 请求超时时间
AKSHARE_RETRY_COUNT = 3  # 重试次数

# CORS配置
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
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

1. 克隆项目
2. 安装依赖
3. 配置数据库
4. 启动服务

### 生产环境部署

1. 使用Gunicorn作为WSGI服务器
2. 配置Nginx反向代理
3. 使用PostgreSQL数据库
4. 配置SSL证书
5. 设置定时任务更新数据

```bash
# 使用Gunicorn启动
gunicorn stock_project.wsgi:application --bind 0.0.0.0:8000

# Docker部署
docker build -t stock-app .
docker run -p 8000:8000 stock-app
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

1. **AKShare数据获取失败**
   - 检查网络连接
   - 确认AKShare版本兼容性
   - 查看API限制和频率

2. **前端无法加载数据**
   - 检查CORS配置
   - 确认API端点正确
   - 查看浏览器控制台错误

3. **数据库连接问题**
   - 检查数据库配置
   - 确认迁移已执行
   - 查看数据库权限

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

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请提交Issue或联系开发者。

---

**注意**: 本项目仅用于学习和研究目的，股票数据仅供参考，不构成投资建议。
