@echo off
echo 🚀 AI智能助手系统快速部署脚本
echo =================================

echo.
echo 📋 选择部署方案：
echo 1. Vercel部署 (推荐 - 最简单)
echo 2. Docker部署 (完整功能)
echo 3. GitHub Pages部署 (静态部署)
echo 4. 查看部署指南
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" goto vercel
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto github
if "%choice%"=="4" goto guide
goto invalid

:vercel
echo.
echo 🌐 开始Vercel部署...
echo.
echo 📝 请确保已安装Node.js和npm
echo 📝 如果没有安装，请访问: https://nodejs.org/
echo.
pause

echo 🔧 安装Vercel CLI...
npm install -g vercel

echo 🔐 登录Vercel...
vercel login

echo 🚀 部署到Vercel...
vercel --prod

echo ✅ Vercel部署完成！
echo 🌐 您的应用已部署到: https://your-app.vercel.app
pause
goto end

:docker
echo.
echo 🐳 开始Docker部署...
echo.
echo 📝 请确保已安装Docker Desktop
echo 📝 如果没有安装，请访问: https://www.docker.com/products/docker-desktop/
echo.
pause

echo 🔧 构建Docker镜像...
docker build -t ai-assistant-system .

echo 🚀 启动Docker容器...
docker run -d -p 8000:8000 --name ai-assistant ai-assistant-system

echo ✅ Docker部署完成！
echo 🌐 本地访问地址: http://localhost:8000
pause
goto end

:github
echo.
echo 📦 开始GitHub Pages部署...
echo.
echo 📝 请确保已有GitHub账户和仓库
echo 📝 如果没有，请先创建GitHub仓库
echo.
pause

echo 🔧 初始化Git仓库...
git init
git add .
git commit -m "Initial commit"

echo 📤 推送到GitHub...
echo 请手动执行以下命令：
echo git remote add origin https://github.com/yourusername/ai-assistant-system.git
echo git push -u origin main
echo.
echo 📋 然后在GitHub仓库设置中启用GitHub Pages
echo ✅ GitHub Pages部署完成！
pause
goto end

:guide
echo.
echo 📚 打开部署指南...
start DEPLOYMENT_GUIDE.md
goto end

:invalid
echo ❌ 无效选择，请重新运行脚本
pause
goto end

:end
echo.
echo 🎉 部署脚本执行完成！
echo 📚 更多信息请查看 DEPLOYMENT_GUIDE.md
pause

