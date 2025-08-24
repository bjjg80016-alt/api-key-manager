#!/usr/bin/env python3
"""
部署脚本
用于自动化部署API密钥管理工具
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令并处理错误"""
    print(f"\n🚀 {description}")
    print(f"执行命令: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 命令执行失败: {result.stderr}")
        return False
    
    print(f"✅ {description} 成功")
    if result.stdout:
        print(result.stdout)
    return True

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
    return True

def create_directories():
    """创建必要的目录"""
    print("📁 创建目录结构...")
    directories = [
        "logs",
        "config",
        "data",
        "backups",
        "static",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖...")
    
    # 升级pip
    run_command("python -m pip install --upgrade pip", "升级pip")
    
    # 安装requirements.txt中的依赖
    if os.path.exists("requirements.txt"):
        run_command("pip install -r requirements.txt", "安装项目依赖")
    else:
        print("❌ requirements.txt文件不存在")
        return False
    
    return True

def setup_config():
    """设置配置文件"""
    print("⚙️ 设置配置文件...")
    
    # 复制示例配置文件
    if os.path.exists("config/api_config.json"):
        print("✅ 配置文件已存在")
    else:
        print("❌ 配置文件不存在，请确保config/api_config.json存在")
        return False
    
    return True

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    
    if os.path.exists("tests"):
        run_command("python -m pytest tests/ -v", "运行单元测试")
    else:
        print("ℹ️ 测试目录不存在，跳过测试")
    
    return True

def start_service():
    """启动服务"""
    print("🎯 启动服务...")
    
    # 启动Web服务
    run_command("python src/web_interface.py", "启动Web服务")
    
    return True

def main():
    """主函数"""
    print("🎬 开始部署API密钥管理工具...")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    if not install_dependencies():
        return False
    
    # 设置配置
    if not setup_config():
        return False
    
    # 运行测试
    if not run_tests():
        return False
    
    print("\n🎉 部署完成！")
    print("=" * 50)
    print("📋 使用说明:")
    print("1. 命令行工具: python api_key_manager.py")
    print("2. Web界面: python src/web_interface.py")
    print("3. 查看日志: tail -f logs/api_manager.log")
    print("4. 配置文件: config/api_config.json")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)