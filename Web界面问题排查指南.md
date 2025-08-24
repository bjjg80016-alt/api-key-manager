# Web界面打不开问题排查指南

## 问题描述
用户反映Web界面无法打开，需要系统性地排查可能的原因。

## 快速诊断
运行诊断脚本获取详细信息：
```bash
python diagnose_web.py
```

## 详细排查步骤

### 1. Python依赖问题

#### 检查方法
```bash
# 检查Python版本
python --version

# 检查依赖包
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
python -c "import jinja2; print('Jinja2 OK')"
```

#### 解决方案
```bash
# 安装依赖
pip install fastapi uvicorn jinja2 python-multipart pydantic

# 或使用项目requirements.txt
pip install -r requirements.txt

# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 端口占用问题

#### 检查方法
```bash
# 检查端口占用
netstat -ano | findstr :8080

# 或使用PowerShell
Get-NetTCPConnection -LocalPort 8080
```

#### 解决方案
```bash
# 更改端口
python start_web.py --port 8081

# 或结束占用进程
taskkill /PID <进程ID> /F

# 使用简单服务器（不同端口）
python simple_server.py
```

### 3. 文件路径问题

#### 检查方法
```bash
# 确保在正确目录
pwd

# 检查必要文件
dir src\web_interface.py
dir config\api_config.json
dir templates\index.html
dir static\css\style.css
```

#### 解决方案
```bash
# 进入项目根目录
cd D:\ai部署

# 检查文件完整性
python -c "import os; [print(f) for f in ['src/web_interface.py', 'config/api_config.json'] if os.path.exists(f)]"
```

### 4. 防火墙/安全软件问题

#### 检查方法
```bash
# 临时关闭防火墙测试
netsh advfirewall set allprofiles state off

# 检查防火墙规则
netsh advfirewall show allprofiles
```

#### 解决方案
```bash
# 添加防火墙例外
netsh advfirewall firewall add rule name="Python Web Server" dir=in action=allow program="python.exe" enable=yes

# 或只允许特定端口
netsh advfirewall firewall add rule name="Web Server Port 8080" dir=in action=allow protocol=TCP localport=8080
```

### 5. 静态文件问题

#### 检查方法
```bash
# 检查静态文件
dir static\css\style.css
dir static\js\app.js

# 检查文件大小
powershell -c "Get-ChildItem -Path static -Recurse | Select-Object Name, Length"
```

#### 解决方案
确保静态文件存在且可读：
```bash
# 重新创建静态文件（如果缺失）
mkdir -p static\css static\js
# 手动创建或复制必要的CSS和JS文件
```

### 6. 配置文件问题

#### 检查方法
```bash
# 检查配置文件格式
python -c "import json; json.load(open('config/api_config.json')); print('Config OK')"
```

#### 解决方案
```bash
# 重置配置文件
echo {"api_keys": {}, "endpoints": {}, "security": {"encrypt_keys": false}, "logging": {"level": "INFO"}} > config\api_config.json
```

## 启动方式

### 方式1: 使用start_web.py
```bash
python start_web.py
```

### 方式2: 使用simple_server.py
```bash
python simple_server.py
```

### 方式3: 直接运行web_interface.py
```bash
python src\web_interface.py
```

### 方式4: 使用uvicorn
```bash
python -m uvicorn src.web_interface:app --reload --host 0.0.0.0 --port 8080
```

## 访问地址

尝试以下地址：
- http://localhost:8080
- http://127.0.0.1:8080
- http://[你的IP地址]:8080

## 健康检查

访问健康检查端点：
- http://localhost:8080/health
- http://localhost:8080/api/keys

## 日志查看

```bash
# 查看应用日志
type logs\api_manager.log

# 实时查看日志
powershell -c "Get-Content logs\api_manager.log -Wait"
```

## 常见错误及解决方案

### 1. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'fastapi'
```
**解决方案**: 安装缺失的依赖包

### 2. Port already in use
```
OSError: [Errno 10048] Address already in use
```
**解决方案**: 更改端口或结束占用进程

### 3. Permission denied
```
PermissionError: [Errno 13] Permission denied
```
**解决方案**: 检查文件权限，以管理员身份运行

### 4. Connection refused
```
ConnectionRefusedError: [Errno 111] Connection refused
```
**解决方案**: 检查防火墙设置，确保服务器已启动

### 5. Template not found
```
jinja2.exceptions.TemplateNotFound: index.html
```
**解决方案**: 检查templates目录和文件路径

## 系统要求

- Python 3.7+
- Windows 10/11
- 至少100MB磁盘空间
- 网络连接（用于外部API）

## 联系支持

如果问题仍然存在，请提供以下信息：
1. 完整的错误日志
2. 运行 `python diagnose_web.py` 的输出
3. 操作系统版本
4. Python版本和已安装的包列表

## 预防措施

1. **使用虚拟环境**: 避免包冲突
2. **定期备份**: 备份配置文件和数据
3. **监控日志**: 定期检查应用日志
4. **安全更新**: 保持依赖包最新
5. **文档记录**: 记录配置更改和问题解决过程