#!/usr/bin/env python3
"""
API密钥管理工具启动脚本
"""

import sys
import os
import json
from pathlib import Path

def main():
    """主启动函数"""
    print("🔑 API密钥管理工具")
    print("=" * 40)
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        sys.exit(1)
    
    # 检查依赖
    try:
        import requests
        import json
        print("✅ 核心依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    
    # 检查配置文件
    config_file = Path("config/api_config.json")
    if not config_file.exists():
        print("⚠️  配置文件不存在，将创建默认配置")
        create_default_config()
    
    # 显示菜单
    show_menu()

def create_default_config():
    """创建默认配置文件"""
    default_config = {
        "api_keys": {},
        "endpoints": {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com"
        },
        "rates": {
            "openai": {"rpm": 60, "tpm": 90000},
            "anthropic": {"rpm": 60, "tpm": 90000}
        },
        "security": {
            "encrypt_keys": True,
            "backup_enabled": True,
            "rotation_days": 90
        }
    }
    
    # 确保config目录存在
    Path("config").mkdir(exist_ok=True)
    
    with open("config/api_config.json", "w", encoding="utf-8") as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 默认配置文件已创建")

def show_menu():
    """显示主菜单"""
    while True:
        print("\n📋 请选择操作:")
        print("1. 🔑 命令行密钥管理")
        print("2. 🌐 启动Web界面")
        print("3. 🧪 运行测试")
        print("4. 📚 查看文档")
        print("5. 📋 部署信息")
        print("6. 🚪 退出")
        
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == "1":
            run_api_manager()
        elif choice == "2":
            run_web_interface()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            show_docs()
        elif choice == "5":
            show_deployment_info()
        elif choice == "6":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重试")

def run_api_manager():
    """运行API密钥管理器"""
    try:
        sys.path.insert(0, 'src')
        from api_key_manager import main as api_manager_main
        api_manager_main()
    except ImportError:
        print("❌ API密钥管理器未找到")
    except Exception as e:
        print(f"❌ 运行API管理器时出错: {e}")

def run_web_interface():
    """运行Web界面"""
    try:
        sys.path.insert(0, 'src')
        from web_interface import main as web_main
        web_main()
    except ImportError:
        print("❌ Web界面未找到，请检查依赖是否安装")
        print("需要安装: pip install fastapi uvicorn jinja2")
    except Exception as e:
        print(f"❌ 运行Web界面时出错: {e}")

def run_tests():
    """运行系统测试"""
    try:
        import subprocess
        print("🧪 运行测试...")
        
        # 检查是否有pytest
        try:
            import pytest
            result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'], 
                                  capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("错误:", result.stderr)
        except ImportError:
            print("❌ pytest未安装，请运行: pip install pytest")
            print("或者手动运行测试文件: python tests/test_api_manager.py")
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")

def show_docs():
    """显示文档"""
    docs = [
        ("README.md", "项目说明"),
        ("DEPLOYMENT.md", "部署指南"),
        ("项目.md", "项目概述"),
        ("claude_project_guide.md", "Claude项目指南")
    ]
    
    print("\n📚 可用文档:")
    for i, (filename, description) in enumerate(docs, 1):
        if Path(filename).exists():
            print(f"{i}. {description} ({filename})")
        else:
            print(f"{i}. {description} ({filename}) - 未找到")
    
    choice = input("\n请选择要查看的文档 (1-4): ").strip()
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= 4:
            filename = docs[choice_num - 1][0]
            if Path(filename).exists():
                with open(filename, "r", encoding="utf-8") as f:
                    print(f"\n📄 {filename} 内容:")
                    print("=" * 50)
                    print(f.read())
            else:
                print(f"❌ 文件 {filename} 不存在")
        else:
            print("❌ 无效选择")
    except ValueError:
        print("❌ 请输入有效数字")

def show_deployment_info():
    """显示部署信息"""
    print("\n📋 部署信息:")
    print("=" * 50)
    print("🎯 项目状态: 已完成部署")
    print("📁 项目结构: ✅ 已创建")
    print("⚙️ 配置文件: ✅ 已配置")
    print("🐳 Docker支持: ✅ 已配置")
    print("🌐 Web界面: ✅ 已实现")
    print("🧪 测试套件: ✅ 已创建")
    print("📚 文档: ✅ 已完成")
    print()
    print("🚀 快速启动:")
    print("1. 命令行工具: python src/api_key_manager.py")
    print("2. Web界面: python src/web_interface.py")
    print("3. Docker: docker-compose up -d")
    print()
    print("📖 API文档: http://localhost:8080/docs")
    print("🔧 配置文件: config/api_config.json")

if __name__ == "__main__":
    main()
