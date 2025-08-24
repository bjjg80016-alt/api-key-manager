@echo off
chcp 65001 >nul
echo 🔍 Web界面问题诊断工具
echo ================================

echo.
echo 1. 检查Python环境...
python --version
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    goto :error
)
echo ✅ Python已安装

echo.
echo 2. 检查当前目录...
echo 当前目录: %CD%
echo.

echo 3. 检查必要文件...
if exist "start_web.py" (
    echo ✅ start_web.py
) else (
    echo ❌ start_web.py
)

if exist "src\web_interface.py" (
    echo ✅ src\web_interface.py
) else (
    echo ❌ src\web_interface.py
)

if exist "config\api_config.json" (
    echo ✅ config\api_config.json
) else (
    echo ❌ config\api_config.json
)

if exist "templates\index.html" (
    echo ✅ templates\index.html
) else (
    echo ❌ templates\index.html
)

if exist "static\css\style.css" (
    echo ✅ static\css\style.css
) else (
    echo ❌ static\css\style.css
)

echo.
echo 4. 检查端口占用...
netstat -ano | findstr ":8080"
if errorlevel 1 (
    echo ✅ 端口8080可用
) else (
    echo ❌ 端口8080被占用
)

echo.
echo 5. 检查Python依赖...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo ❌ FastAPI未安装
) else (
    echo ✅ FastAPI已安装
)

python -c "import uvicorn" 2>nul
if errorlevel 1 (
    echo ❌ Uvicorn未安装
) else (
    echo ✅ Uvicorn已安装
)

python -c "import jinja2" 2>nul
if errorlevel 1 (
    echo ❌ Jinja2未安装
) else (
    echo ✅ Jinja2已安装
)

echo.
echo 6. 测试网络连接...
ping -n 1 127.0.0.1 >nul
if errorlevel 1 (
    echo ❌ 本地网络连接失败
) else (
    echo ✅ 本地网络连接正常
)

echo.
echo ================================
echo 📋 诊断完成
echo.
echo 如果发现问题，请运行修复脚本:
echo python fix_web.py
echo.
echo 或手动启动Web界面:
echo python start_web.py
echo python simple_server.py
echo ================================

goto :end

:error
echo.
echo ❌ 诊断发现错误，请检查上述信息
pause
exit /b 1

:end
pause