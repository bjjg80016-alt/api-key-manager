#!/usr/bin/env python3
"""
智能Web服务启动器
自动检测环境并启动最适合的服务
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_package(package_name):
    """安装Python包"""
    try:
        print(f"📦 安装 {package_name}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {package_name} 安装成功")
        return True
    except subprocess.CalledProcessError:
        try:
            # 尝试使用pip
            subprocess.check_call(['pip', 'install', package_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {package_name} 安装成功 (pip)")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ {package_name} 安装失败")
            return False

def check_dependencies():
    """检查并安装依赖"""
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'jinja2': 'Jinja2',
        'python_multipart': 'Python-Multipart'
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {name} 已安装")
        except ImportError:
            print(f"❌ {name} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 需要安装 {len(missing_packages)} 个包...")
        for package in missing_packages:
            if not install_package(package):
                return False
    
    return True

def check_port(port):
    """检查端口是否被占用"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8080, max_attempts=10):
    """找到可用的端口"""
    for i in range(max_attempts):
        port = start_port + i
        if check_port(port):
            return port
    return None

def start_full_service(port):
    """启动完整的FastAPI服务"""
    try:
        print(f"🚀 启动完整Web服务 (端口 {port})...")
        
        # 添加src目录到Python路径
        sys.path.insert(0, 'src')
        
        # 导入并启动Web界面
        from web_interface import create_app
        import uvicorn
        
        app = create_app()
        
        print(f"📍 服务地址: http://localhost:{port}")
        print(f"📖 API文档: http://localhost:{port}/docs")
        print(f"💚 健康检查: http://localhost:{port}/health")
        
        # 等待一秒后打开浏览器
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{port}')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # 启动服务
        uvicorn.run(app, host='127.0.0.1', port=port, log_level='info')
        
    except Exception as e:
        print(f"❌ 完整服务启动失败: {e}")
        return False
    
    return True

def start_simple_service(port):
    """启动简单的HTTP服务"""
    try:
        print(f"🚀 启动简化Web服务 (端口 {port})...")
        
        import http.server
        import socketserver
        
        class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
        
        with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
            print(f"📍 服务地址: http://localhost:{port}")
            
            # 等待一秒后打开浏览器
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}')
            
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print("🎉 服务启动成功！按 Ctrl+C 停止服务")
            httpd.serve_forever()
        
    except Exception as e:
        print(f"❌ 简化服务启动失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🌐 API密钥管理器 - 智能Web服务启动器")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 检查必要文件
    required_files = [
        'src/web_interface.py',
        'src/api_key_manager.py',
        'templates/index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有必要文件存在")
    
    # 创建必要的目录
    for directory in ['logs', 'data', 'backups']:
        Path(directory).mkdir(exist_ok=True)
    
    # 尝试启动完整服务
    port = find_available_port()
    if port is None:
        print("❌ 无法找到可用端口")
        return False
    
    print(f"✅ 找到可用端口: {port}")
    
    # 检查依赖
    if check_dependencies():
        print("\n🚀 启动完整服务...")
        if start_full_service(port):
            return True
        else:
            print("\n⚠️ 完整服务启动失败，尝试简化服务...")
    
    # 如果完整服务失败，启动简化服务
    print("\n🚀 启动简化服务...")
    simple_port = find_available_port(8000)
    if simple_port and start_simple_service(simple_port):
        return True
    
    print("❌ 所有服务启动失败")
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n💡 提示:")
            print("1. 确保Python已正确安装")
            print("2. 检查网络连接")
            print("3. 尝试以管理员身份运行")
            print("4. 可以直接打开 quick_start.html 文件")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        sys.exit(0)