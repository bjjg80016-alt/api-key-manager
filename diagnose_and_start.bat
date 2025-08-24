@echo off
chcp 65001 >nul
title API密钥管理器 - 问题诊断
echo 🔍 API密钥管理器 - 问题诊断工具
echo ========================================
echo.

cd /d "%~dp0"

echo 📋 正在诊断问题...
echo.

echo 1. 检查Python环境:
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    echo 请安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    goto end
) else (
    echo ✅ Python环境正常
)

echo.
echo 2. 检查端口占用:
netstat -ano | findstr :8080
if %errorlevel% equ 0 (
    echo ⚠️ 端口8080被占用
    echo 尝试使用端口8081...
    set USE_PORT=8081
) else (
    echo ✅ 端口8080可用
    set USE_PORT=8080
)

echo.
echo 3. 检查必要文件:
if exist "src\web_interface.py" (
    echo ✅ web_interface.py 存在
) else (
    echo ❌ web_interface.py 不存在
)

if exist "templates\index.html" (
    echo ✅ index.html 存在
) else (
    echo ❌ index.html 不存在
)

echo.
echo 4. 尝试启动最简单的HTTP服务:
echo.
echo 🚀 启动简单HTTP服务器...
echo 📍 请访问: http://localhost:%USE_PORT%
echo 💚 或者直接访问: http://127.0.0.1:%USE_PORT%
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

:: 启动最简单的HTTP服务器
python -m http.server %USE_PORT% --bind 127.0.0.1

:end
echo.
pause