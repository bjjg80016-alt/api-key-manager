@echo off
chcp 65001 >nul
echo 🌐 API密钥管理器 - 简化启动工具
echo ========================================

echo 📋 正在启动简化Web服务器...
echo 📍 访问地址: http://localhost:8000
echo 💚 健康检查: http://localhost:8000/health
echo 按 Ctrl+C 停止服务器
echo ========================================

cd /d "%~dp0"

python -m http.server 8000 --bind 127.0.0.1

pause