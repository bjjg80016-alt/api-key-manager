@echo off
chcp 65001 >nul
echo 🚀 启动API密钥管理器Web界面
echo ================================

echo.
echo 1. 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python
    pause
    exit /b 1
)
echo ✅ Python已安装

echo.
echo 2. 检查依赖包...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo ❌ FastAPI未安装，正在安装...
    python -m pip install fastapi uvicorn jinja2 python-multipart
) else (
    echo ✅ 依赖包已安装
)

echo.
echo 3. 检查端口占用...
netstat -ano | findstr ":8080"
if errorlevel 1 (
    echo ✅ 端口8080可用
) else (
    echo ❌ 端口8080被占用，尝试使用端口8081
    set PORT=8081
    goto :start_server
)

set PORT=8080

:start_server
echo.
echo 4. 启动Web界面...
echo 访问地址: http://localhost:%PORT%
echo 健康检查: http://localhost:%PORT%/health
echo API文档: http://localhost:%PORT%/docs
echo.
echo 按Ctrl+C停止服务器
echo ================================

:: 尝试启动FastAPI服务器
python start_web.py --port %PORT%
if errorlevel 1 (
    echo.
    echo FastAPI启动失败，尝试简单服务器...
    python simple_server.py
)

pause