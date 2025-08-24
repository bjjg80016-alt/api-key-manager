@echo off
chcp 65001 >nul
title API密钥管理器 - 一键启动
echo 🌐 API密钥管理器 - 一键启动
echo ========================================
echo.

cd /d "%~dp0"

echo 🚀 正在启动最简单的Web服务...
echo.
echo 📍 服务地址:
echo    http://localhost:8000
echo    http://127.0.0.1:8000
echo.
echo 💡 提示:
echo    - 服务启动后会自动打开浏览器
echo    - 按 Ctrl+C 停止服务
echo    - 如果8000端口被占用，会自动使用8001
echo.
echo ========================================
echo.

:: 检查8000端口
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ⚠️ 端口8000被占用，使用端口8001
    set PORT=8001
) else (
    echo ✅ 端口8000可用
    set PORT=8000
)

:: 启动HTTP服务器
python -m http.server %PORT% --bind 127.0.0.1

pause