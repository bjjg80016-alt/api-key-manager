@echo off
chcp 65001 >nul
echo 🌐 API密钥管理器 - Web界面修复工具
echo ========================================

echo 📋 步骤1: 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.8+
    pause
    exit /b 1
) else (
    echo ✅ Python环境正常
)

echo 📋 步骤2: 安装必要依赖
echo 正在安装FastAPI...
pip install fastapi >nul 2>&1
echo 正在安装Uvicorn...
pip install uvicorn >nul 2>&1
echo 正在安装Jinja2...
pip install jinja2 >nul 2>&1
echo 正在安装Python-Multipart...
pip install python-multipart >nul 2>&1
echo ✅ 依赖安装完成

echo 📋 步骤3: 检查端口占用
netstat -ano | findstr :8080 >nul
if %errorlevel% equ 0 (
    echo ⚠️  端口8080被占用，尝试使用8081端口
    set PORT=8081
) else (
    echo ✅ 端口8080可用
    set PORT=8080
)

echo 📋 步骤4: 创建必要的目录和文件
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "backups" mkdir backups

echo 📋 步骤5: 启动Web界面
echo 🚀 启动中...
echo 📍 访问地址: http://localhost:%PORT%
echo 💚 健康检查: http://localhost:%PORT%/health
echo 📖 API文档: http://localhost:%PORT%/docs
echo 按 Ctrl+C 停止服务器
echo ========================================

python src\web_interface.py --port %PORT%

pause