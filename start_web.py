#!/usr/bin/env python3
"""
简化的Web界面启动器
如果FastAPI未安装，会提示安装
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = ['fastapi', 'uvicorn', 'jinja2', 'python-multipart']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("\n请安装以下依赖:")
        print("pip install fastapi uvicorn jinja2 python-multipart")
        return False
    
    return True

def start_web_interface():
    """启动Web界面"""
    try:
        # 添加src目录到Python路径
        sys.path.insert(0, 'src')
        
        from web_interface import main as web_main
        web_main()
        
    except Exception as e:
        print(f"❌ 启动Web界面失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🌐 API密钥管理器 - Web界面")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        print("\n💡 安装依赖后重试:")
        print("pip install fastapi uvicorn jinja2 python-multipart")
        return False
    
    # 检查必要文件
    required_files = [
        'src/web_interface.py',
        'src/api_key_manager.py',
        'config/api_config.json',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 所有依赖和文件检查通过")
    print("🚀 启动Web界面...")
    
    # 启动Web界面
    return start_web_interface()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)