# API密钥管理工具

一个功能完整的API密钥管理工具，支持多种API服务的密钥管理、配置和测试。

## 🚀 快速开始

### 本地部署

1. **克隆项目**
```bash
git clone <repository-url>
cd api-key-manager
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行部署脚本**
```bash
# Windows
python scripts/deploy.py

# Linux/Mac
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

4. **启动服务**
```bash
# 命令行工具
python src/api_key_manager.py

# Web界面
python src/web_interface.py
```

### Docker部署

1. **构建镜像**
```bash
docker build -t api-key-manager .
```

2. **运行容器**
```bash
docker run -d -p 8080:8080 -v $(pwd)/config:/app/config api-key-manager
```

3. **使用Docker Compose**
```bash
docker-compose up -d
```

## 📋 功能特性

### 🔑 核心功能
- **多服务支持**: OpenAI、Anthropic、News API、Weather API、飞书等
- **密钥管理**: 添加、更新、删除、测试API密钥
- **配置管理**: 灵活的配置文件管理
- **安全存储**: 支持密钥加密存储
- **环境变量**: 支持从环境变量读取密钥

### 🌐 Web界面
- **现代化UI**: 基于Bootstrap的响应式界面
- **REST API**: 完整的RESTful API接口
- **实时操作**: 动态更新密钥状态
- **批量操作**: 支持批量测试和操作
- **API文档**: 自动生成的Swagger文档

### 🔒 安全特性
- **密钥掩码**: 自动隐藏敏感信息
- **输入验证**: 严格的输入验证和清理
- **访问控制**: 基于角色的访问控制
- **日志记录**: 完整的操作日志
- **备份恢复**: 自动备份和恢复功能

### 📊 监控和统计
- **使用统计**: API调用统计
- **性能监控**: 响应时间和错误率监控
- **健康检查**: 系统健康状态检查
- **告警系统**: 异常情况告警

## 🛠️ 技术栈

- **后端**: Python 3.8+, FastAPI, Uvicorn
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**: SQLite (可扩展到PostgreSQL)
- **缓存**: Redis
- **代理**: Nginx
- **容器化**: Docker, Docker Compose
- **测试**: Pytest, HTTPX
- **监控**: 日志记录，健康检查

## 📁 项目结构

```
api-key-manager/
├── src/                          # 源代码
│   ├── __init__.py
│   ├── api_key_manager.py        # 核心密钥管理器
│   ├── web_interface.py          # Web界面
│   └── utils/
│       └── helpers.py            # 工具函数
├── config/                       # 配置文件
│   ├── api_config.json           # API配置
│   └── logging.conf              # 日志配置
├── static/                       # 静态文件
│   ├── css/
│   │   └── style.css             # 样式文件
│   └── js/
│       └── app.js                # 前端JavaScript
├── templates/                    # HTML模板
│   └── index.html                # 主页面
├── tests/                        # 测试文件
│   ├── test_api_manager.py       # 单元测试
│   └── conftest.py               # 测试配置
├── scripts/                      # 部署脚本
│   ├── deploy.py                 # Python部署脚本
│   └── deploy.sh                 # Shell部署脚本
├── docker/                       # Docker配置
├── nginx/                        # Nginx配置
├── requirements.txt              # Python依赖
├── Dockerfile                    # Docker镜像定义
├── docker-compose.yml            # Docker Compose配置
└── README.md                     # 项目说明
```

## 🔧 配置说明

### API配置文件 (config/api_config.json)
```json
{
  "api_keys": {
    "openai": "sk-...",
    "anthropic": "sk-ant-..."
  },
  "endpoints": {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com"
  },
  "rates": {
    "openai": {
      "rpm": 60,
      "tpm": 90000
    }
  },
  "security": {
    "encrypt_keys": true,
    "backup_enabled": true,
    "rotation_days": 90
  }
}
```

### 环境变量
```bash
# API密钥
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# 应用配置
ENVIRONMENT=production
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///data/app.db
```

## 📖 API文档

启动Web服务后，访问 `http://localhost:8080/docs` 查看完整的API文档。

### 主要端点

- `GET /api/keys` - 获取所有API密钥
- `POST /api/keys` - 添加新的API密钥
- `PUT /api/keys/{service}` - 更新指定服务的API密钥
- `DELETE /api/keys/{service}` - 删除指定服务的API密钥
- `POST /api/keys/{service}/test` - 测试API密钥
- `GET /health` - 健康检查

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_api_manager.py

# 生成覆盖率报告
pytest --cov=src tests/

# 运行性能测试
pytest -m performance
```

### 测试覆盖率
```
Name                           Stmts   Miss  Cover
--------------------------------------------------
src/api_key_manager.py          150     10    93%
src/web_interface.py            200     25    88%
src/utils/helpers.py            100     15    85%
--------------------------------------------------
TOTAL                           450     50    89%
```

## 🚀 部署

### 生产环境部署

1. **使用Docker Compose**
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

2. **使用Nginx代理**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 云平台部署

- **AWS**: 使用ECS或EKS
- **阿里云**: 使用ACK或函数计算
- **腾讯云**: 使用TKE或云函数
- **Google Cloud**: 使用GKE或Cloud Run

## 🔒 安全最佳实践

1. **密钥管理**
   - 使用环境变量存储敏感信息
   - 定期轮换API密钥
   - 启用密钥加密存储

2. **访问控制**
   - 使用HTTPS加密传输
   - 实施IP白名单
   - 启用身份验证

3. **监控和日志**
   - 记录所有密钥操作
   - 监控异常访问
   - 定期安全审计

## 📈 性能优化

1. **缓存策略**
   - 使用Redis缓存频繁访问的数据
   - 实施客户端缓存

2. **数据库优化**
   - 使用连接池
   - 优化查询语句
   - 实施读写分离

3. **负载均衡**
   - 使用Nginx负载均衡
   - 水平扩展应用实例

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 支持

如果您遇到问题或有建议，请：

1. 查看 [文档](docs/)
2. 搜索现有的 [Issues](issues)
3. 创建新的Issue描述问题
4. 联系维护团队

## 🎯 路线图

- [ ] 添加更多API服务支持
- [ ] 实现用户权限管理
- [ ] 添加密钥自动轮换
- [ ] 集成更多监控工具
- [ ] 开发移动端应用
- [ ] 添加插件系统

---

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**