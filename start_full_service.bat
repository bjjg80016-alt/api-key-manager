@echo off
chcp 65001 >nul
title API密钥管理器 - 完整Web服务
echo 🌐 API密钥管理器 - 完整Web服务启动器
echo ========================================
echo.

cd /d "%~dp0"

echo 📋 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未找到！
    echo 请确保Python已安装并添加到PATH
    echo.
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python环境正常
)

echo.
echo 📦 正在检查和安装依赖...
echo.

:: 检查并安装fastapi
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 FastAPI...
    python -m pip install fastapi >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ FastAPI 安装成功
    ) else (
        echo ❌ FastAPI 安装失败，尝试使用 pip...
        pip install fastapi >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ FastAPI 安装成功 (pip)
        ) else (
            echo ❌ 依赖安装失败，将使用简化版本
            goto start_simple
        )
    )
) else (
    echo ✅ FastAPI 已安装
)

:: 检查并安装uvicorn
python -c "import uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 Uvicorn...
    python -m pip install uvicorn >nul 2>&1
    if %errorlevel% neq 0 (
        pip install uvicorn >nul 2>&1
    )
) else (
    echo ✅ Uvicorn 已安装
)

:: 检查并安装jinja2
python -c "import jinja2" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 Jinja2...
    python -m pip install jinja2 >nul 2>&1
    if %errorlevel% neq 0 (
        pip install jinja2 >nul 2>&1
    )
) else (
    echo ✅ Jinja2 已安装
)

:: 检查并安装python-multipart
python -c "import python_multipart" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装 python-multipart...
    python -m pip install python-multipart >nul 2>&1
    if %errorlevel% neq 0 (
        pip install python-multipart >nul 2>&1
    )
) else (
    echo ✅ python-multipart 已安装
)

echo.
echo 🚀 启动完整Web服务...
echo.

:: 检查端口占用
netstat -ano | findstr :8080 >nul
if %errorlevel% equ 0 (
    echo ⚠️  端口8080被占用，使用端口8081
    set PORT=8081
) else (
    echo ✅ 端口8080可用
    set PORT=8080
)

:: 创建必要的目录
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "backups" mkdir backups

echo.
echo 📍 服务信息：
echo    访问地址：http://localhost:%PORT%
echo    API文档：http://localhost:%PORT%/docs
echo    健康检查：http://localhost:%PORT%/health
echo.
echo 💡 提示：
echo    - 服务启动后会在浏览器中自动打开
echo    - 按 Ctrl+C 停止服务
echo    - 首次启动可能需要几秒钟
echo.
echo ========================================
echo.

:: 尝试启动完整服务
python src\web_interface.py --port %PORT%

if %errorlevel% neq 0 (
    echo.
    echo ❌ 完整服务启动失败，尝试启动简化服务...
    goto start_simple
)

goto end

:start_simple
echo.
echo 🚀 启动简化Web服务...
echo.
echo 📍 服务信息：
echo    访问地址：http://localhost:8000
echo.
echo ========================================
echo.

python -m http.server 8000 --bind 127.0.0.1

:end
pause