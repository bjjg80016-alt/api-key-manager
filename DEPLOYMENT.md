# API 密钥管理工具部署方案

## 项目概述
这是一个功能完整的 API 密钥管理工具，支持多种 API 服务的密钥管理、配置和测试。

## 部署方式

### 1. 本地部署
```bash
# 克隆项目
git clone <repository-url>
cd api-key-manager

# 安装依赖
pip install -r requirements.txt

# 运行
python api_key_manager.py
```

### 2. Docker 部署
```bash
# 构建镜像
docker build -t api-key-manager .

# 运行容器
docker run -d -p 8080:8080 -v $(pwd)/config:/app/config api-key-manager
```

### 3. 云服务器部署
支持 AWS、阿里云、腾讯云等主流云平台

## 项目结构
```
api-key-manager/
├── src/
│   ├── __init__.py
│   ├── api_key_manager.py
│   ├── web_interface.py
│   └── utils/
├── config/
│   ├── api_config.json
│   └── logging.conf
├── tests/
├── docker/
├── scripts/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 功能特性
- 🔑 多服务 API 密钥管理
- 🌐 Web 界面支持
- 🔒 安全的密钥存储
- 📊 密钥使用统计
- 🔄 自动密钥轮换
- 🚀 Docker 容器化部署
- 📋 REST API 接口

## 支持的服务
- OpenAI
- Anthropic
- News API
- Weather API
- 飞书 Webhook
- 自定义 API 服务