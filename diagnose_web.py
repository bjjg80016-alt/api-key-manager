#!/usr/bin/env python3
"""
Web界面问题诊断脚本
用于排查Web界面无法打开的问题
"""

import sys
import os
import json
import socket
import subprocess
from pathlib import Path

def check_python_environment():
    """检查Python环境"""
    print("🔍 检查Python环境...")
    print(f"Python版本: {sys.version}")
    print(f"Python可执行文件: {sys.executable}")
    print(f"Python路径: {sys.path}")
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")
    required_packages = {
        'fastapi': 'FastAPI Web框架',
        'uvicorn': 'ASGI服务器',
        'jinja2': '模板引擎',
        'pydantic': '数据验证',
        'python-multipart': 'multipart支持'
    }
    
    missing_packages = []
    available_packages = []
    
    for package, description in required_packages.items():
        try:
            if package == 'python-multipart':
                import multipart
            else:
                __import__(package)
            available_packages.append(f"✅ {package} - {description}")
        except ImportError:
            missing_packages.append(f"❌ {package} - {description}")
    
    for item in available_packages:
        print(item)
    
    for item in missing_packages:
        print(item)
    
    return len(missing_packages) == 0

def check_files():
    """检查必要文件"""
    print("\n🔍 检查必要文件...")
    required_files = [
        'start_web.py',
        'src/web_interface.py',
        'src/api_key_manager.py',
        'config/api_config.json',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(f"✅ {file_path}")
        else:
            missing_files.append(f"❌ {file_path}")
    
    for item in existing_files:
        print(item)
    
    for item in missing_files:
        print(item)
    
    return len(missing_files) == 0

def check_port_availability():
    """检查端口可用性"""
    print("\n🔍 检查端口可用性...")
    port = 8080
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                print(f"❌ 端口 {port} 被占用")
                return False
            else:
                print(f"✅ 端口 {port} 可用")
                return True
    except Exception as e:
        print(f"❌ 检查端口失败: {e}")
        return False

def check_config_file():
    """检查配置文件"""
    print("\n🔍 检查配置文件...")
    config_file = 'config/api_config.json'
    
    if not Path(config_file).exists():
        print(f"❌ 配置文件不存在: {config_file}")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"✅ 配置文件格式正确")
        print(f"   - 配置的API服务: {list(config.get('api_keys', {}).keys())}")
        print(f"   - 加密设置: {config.get('security', {}).get('encrypt_keys', False)}")
        print(f"   - 日志级别: {config.get('logging', {}).get('level', 'INFO')}")
        
        return True
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

def check_static_files():
    """检查静态文件"""
    print("\n🔍 检查静态文件...")
    static_files = [
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    for file_path in static_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} 不存在")
    
    return all(Path(f).exists() for f in static_files)

def test_simple_server():
    """测试简单服务器"""
    print("\n🔍 测试简单服务器...")
    
    try:
        # 测试导入simple_server模块
        sys.path.insert(0, '.')
        import simple_server
        print("✅ simple_server模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ simple_server模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试简单服务器失败: {e}")
        return False

def check_network_connectivity():
    """检查网络连接"""
    print("\n🔍 检查网络连接...")
    
    try:
        # 测试本地回环
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('127.0.0.1', 80))
            print("✅ 本地回环连接正常")
        
        # 测试DNS解析
        socket.gethostbyname('localhost')
        print("✅ DNS解析正常")
        
        return True
    except Exception as e:
        print(f"❌ 网络连接问题: {e}")
        return False

def check_firewall_permissions():
    """检查防火墙权限（Windows）"""
    print("\n🔍 检查防火墙权限...")
    
    if sys.platform != 'win32':
        print("ℹ️ 非Windows系统，跳过防火墙检查")
        return True
    
    try:
        # 检查Python是否有网络权限
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ 可以访问防火墙配置")
            print("💡 请确保Python有网络访问权限")
        else:
            print("❌ 无法访问防火墙配置")
        
        return True
    except Exception as e:
        print(f"❌ 检查防火墙失败: {e}")
        return False

def generate_recommendations():
    """生成建议"""
    print("\n" + "="*60)
    print("📋 问题排查建议")
    print("="*60)
    
    print("\n1. Python依赖问题:")
    print("   - 安装依赖: pip install fastapi uvicorn jinja2 python-multipart")
    print("   - 使用虚拟环境: python -m venv venv")
    print("   - 激活虚拟环境: venv\\Scripts\\activate")
    
    print("\n2. 端口占用问题:")
    print("   - 检查端口占用: netstat -ano | findstr :8080")
    print("   - 更改端口: python start_web.py --port 8081")
    print("   - 使用简单服务器: python simple_server.py")
    
    print("\n3. 文件路径问题:")
    print("   - 确保在项目根目录运行")
    print("   - 检查文件权限")
    print("   - 验证文件完整性")
    
    print("\n4. 防火墙/安全软件:")
    print("   - 临时关闭防火墙测试")
    print("   - 添加Python到防火墙例外")
    print("   - 检查杀毒软件拦截")
    
    print("\n5. 启动方式:")
    print("   - 方式1: python start_web.py")
    print("   - 方式2: python simple_server.py")
    print("   - 方式3: python src/web_interface.py")
    
    print("\n6. 访问地址:")
    print("   - http://localhost:8080")
    print("   - http://127.0.0.1:8080")
    print("   - http://[你的IP]:8080")

def main():
    """主函数"""
    print("🔧 Web界面问题诊断工具")
    print("="*60)
    
    # 执行所有检查
    checks = [
        ("Python环境", check_python_environment),
        ("依赖包", check_dependencies),
        ("必要文件", check_files),
        ("端口可用性", check_port_availability),
        ("配置文件", check_config_file),
        ("静态文件", check_static_files),
        ("简单服务器", test_simple_server),
        ("网络连接", check_network_connectivity),
        ("防火墙权限", check_firewall_permissions)
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name}检查失败: {e}")
            results[check_name] = False
    
    # 总结
    print("\n" + "="*60)
    print("📊 诊断结果总结")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{check_name}: {status}")
    
    print(f"\n总体结果: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("🎉 所有检查通过，Web界面应该可以正常启动")
    else:
        print("⚠️ 存在问题，请查看上述详细信息和建议")
    
    # 生成建议
    generate_recommendations()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)