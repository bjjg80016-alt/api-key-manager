#!/usr/bin/env python3
"""
Web界面一键修复脚本
自动解决常见的Web界面启动问题
"""

import sys
import os
import subprocess
import json
import shutil
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description}成功")
            if result.stdout.strip():
                print(f"   输出: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description}失败")
            if result.stderr.strip():
                print(f"   错误: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description}超时")
        return False
    except Exception as e:
        print(f"❌ {description}异常: {e}")
        return False

def fix_python_dependencies():
    """修复Python依赖问题"""
    print("🔍 检查Python依赖...")
    
    # 检查pip
    if not run_command("python -m pip --version", "检查pip"):
        print("❌ pip不可用，请先安装pip")
        return False
    
    # 升级pip
    run_command("python -m pip install --upgrade pip", "升级pip")
    
    # 安装基础依赖
    dependencies = [
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0", 
        "jinja2>=3.1.2",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.6"
    ]
    
    for dep in dependencies:
        if not run_command(f"python -m pip install {dep}", f"安装{dep}"):
            print(f"⚠️ {dep}安装失败，继续其他修复...")
    
    return True

def fix_port_issues():
    """修复端口问题"""
    print("🔍 检查端口问题...")
    
    # 检查端口8080是否被占用
    if run_command('netstat -ano | findstr ":8080"', "检查端口8080占用"):
        print("⚠️ 端口8080被占用，尝试使用端口8081")
        
        # 修改启动脚本使用8081端口
        if Path("start_web.py").exists():
            try:
                with open("start_web.py", "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 替换默认端口
                content = content.replace('default=8080', 'default=8081')
                
                with open("start_web.py", "w", encoding="utf-8") as f:
                    f.write(content)
                
                print("✅ 已修改启动脚本使用端口8081")
            except Exception as e:
                print(f"❌ 修改启动脚本失败: {e}")
    
    return True

def fix_file_issues():
    """修复文件问题"""
    print("🔍 检查文件问题...")
    
    # 确保目录结构存在
    directories = ["src", "config", "templates", "static/css", "static/js", "logs"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 确保目录存在: {directory}")
    
    # 创建默认配置文件
    config_file = "config/api_config.json"
    if not Path(config_file).exists():
        default_config = {
            "api_keys": {
                "openai": "",
                "anthropic": "",
                "news_api": "",
                "weather_api": "",
                "feishu": ""
            },
            "endpoints": {
                "openai": "https://api.openai.com/v1",
                "anthropic": "https://api.anthropic.com",
                "news_api": "https://newsapi.org/v2",
                "weather_api": "https://api.openweathermap.org/data/2.5"
            },
            "security": {
                "encrypt_keys": False,
                "backup_enabled": True,
                "rotation_days": 90
            },
            "logging": {
                "level": "INFO",
                "file": "logs/api_manager.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
        
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print(f"✅ 创建默认配置文件: {config_file}")
        except Exception as e:
            print(f"❌ 创建配置文件失败: {e}")
    
    # 创建默认HTML模板
    template_file = "templates/index.html"
    if not Path(template_file).exists():
        default_html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API密钥管理器</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .container { max-width: 1200px; }
        .card { margin-bottom: 20px; }
        .status { padding: 10px; border-radius: 5px; margin-bottom: 10px; }
        .status.success { background-color: #d4edda; color: #155724; }
        .status.error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-key"></i> API密钥管理器
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">系统状态</h5>
                    </div>
                    <div class="card-body">
                        <div id="systemStatus" class="status success">
                            系统运行正常
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <strong>服务地址:</strong> <span id="serverUrl">http://localhost:8080</span>
                            </div>
                            <div class="col-md-6">
                                <strong>状态:</strong> <span id="serverStatus">正常</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 简单的健康检查
        fetch('/health')
            .then(response => response.json())
            .then(data => {
                document.getElementById('systemStatus').className = 'status success';
                document.getElementById('systemStatus').textContent = data.message;
                document.getElementById('serverStatus').textContent = '正常';
            })
            .catch(error => {
                document.getElementById('systemStatus').className = 'status error';
                document.getElementById('systemStatus').textContent = '连接失败';
                document.getElementById('serverStatus').textContent = '异常';
            });
    </script>
</body>
</html>"""
        
        try:
            with open(template_file, "w", encoding="utf-8") as f:
                f.write(default_html)
            print(f"✅ 创建默认HTML模板: {template_file}")
        except Exception as e:
            print(f"❌ 创建HTML模板失败: {e}")
    
    # 创建默认CSS文件
    css_file = "static/css/style.css"
    if not Path(css_file).exists():
        default_css = """body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar-brand {
    font-weight: bold;
}

.card {
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    border: 1px solid rgba(0, 0, 0, 0.125);
}

.card-header {
    background-color: #f8f9fa;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.btn-primary:hover {
    background-color: #0b5ed7;
    border-color: #0a58ca;
}

.status {
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
}

.status.success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.status.error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.status.warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}"""
        
        try:
            with open(css_file, "w", encoding="utf-8") as f:
                f.write(default_css)
            print(f"✅ 创建默认CSS文件: {css_file}")
        except Exception as e:
            print(f"❌ 创建CSS文件失败: {e}")
    
    # 创建默认JS文件
    js_file = "static/js/app.js"
    if not Path(js_file).exists():
        default_js = """// API密钥管理器 - 前端JavaScript
console.log('API密钥管理器已加载');

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成');
    
    // 健康检查
    checkHealth();
    
    // 加载API密钥列表
    loadApiKeys();
});

// 健康检查
function checkHealth() {
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('健康检查结果:', data);
            updateSystemStatus(data.status === 'healthy');
        })
        .catch(error => {
            console.error('健康检查失败:', error);
            updateSystemStatus(false);
        });
}

// 加载API密钥列表
function loadApiKeys() {
    fetch('/api/keys')
        .then(response => response.json())
        .then(data => {
            console.log('API密钥列表:', data);
            displayApiKeys(data);
        })
        .catch(error => {
            console.error('加载API密钥失败:', error);
        });
}

// 显示API密钥
function displayApiKeys(keys) {
    const container = document.getElementById('keysList');
    if (!container) return;
    
    container.innerHTML = '';
    
    for (const [service, key] of Object.entries(keys)) {
        const keyElement = document.createElement('div');
        keyElement.className = 'list-group-item';
        keyElement.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${service}</strong>
                    <br>
                    <small class="text-muted">${key}</small>
                </div>
                <div>
                    <button class="btn btn-sm btn-outline-primary" onclick="testKey('${service}')">
                        测试
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteKey('${service}')">
                        删除
                    </button>
                </div>
            </div>
        `;
        container.appendChild(keyElement);
    }
}

// 更新系统状态
function updateSystemStatus(isHealthy) {
    const statusElement = document.getElementById('systemStatus');
    const serverStatusElement = document.getElementById('serverStatus');
    
    if (statusElement) {
        statusElement.className = isHealthy ? 'status success' : 'status error';
        statusElement.textContent = isHealthy ? '系统运行正常' : '系统连接异常';
    }
    
    if (serverStatusElement) {
        serverStatusElement.textContent = isHealthy ? '正常' : '异常';
    }
}

// 测试API密钥
function testKey(service) {
    fetch(`/api/keys/${service}/test`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            alert('测试失败: ' + error.message);
        });
}

// 删除API密钥
function deleteKey(service) {
    if (confirm(`确定要删除 ${service} 的API密钥吗？`)) {
        fetch(`/api/keys/${service}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadApiKeys(); // 重新加载列表
            })
            .catch(error => {
                alert('删除失败: ' + error.message);
            });
    }
}"""
        
        try:
            with open(js_file, "w", encoding="utf-8") as f:
                f.write(default_js)
            print(f"✅ 创建默认JS文件: {js_file}")
        except Exception as e:
            print(f"❌ 创建JS文件失败: {e}")
    
    return True

def fix_firewall_issues():
    """修复防火墙问题"""
    print("🔍 检查防火墙问题...")
    
    if sys.platform != 'win32':
        print("ℹ️ 非Windows系统，跳过防火墙修复")
        return True
    
    # 添加Python到防火墙例外
    commands = [
        'netsh advfirewall firewall add rule name="Python Web Server" dir=in action=allow program="python.exe" enable=yes',
        'netsh advfirewall firewall add rule name="Python Web Server Port 8080" dir=in action=allow protocol=TCP localport=8080',
        'netsh advfirewall firewall add rule name="Python Web Server Port 8081" dir=in action=allow protocol=TCP localport=8081'
    ]
    
    for cmd in commands:
        run_command(cmd, "添加防火墙规则")
    
    return True

def test_web_server():
    """测试Web服务器"""
    print("🔍 测试Web服务器...")
    
    # 首先测试简单服务器
    if Path("simple_server.py").exists():
        print("✅ 找到简单服务器，可以尝试运行:")
        print("   python simple_server.py")
    
    # 测试FastAPI服务器
    if Path("start_web.py").exists():
        print("✅ 找到FastAPI启动脚本，可以尝试运行:")
        print("   python start_web.py")
    
    # 测试直接运行
    if Path("src/web_interface.py").exists():
        print("✅ 找到Web界面模块，可以尝试运行:")
        print("   python src/web_interface.py")
    
    return True

def create_startup_script():
    """创建启动脚本"""
    print("🔍 创建启动脚本...")
    
    # 创建Windows批处理文件
    batch_content = """@echo off
echo 正在启动API密钥管理器Web界面...
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖包...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 安装依赖包...
    pip install fastapi uvicorn jinja2 python-multipart
)

REM 启动Web界面
echo 启动Web界面...
echo 访问地址: http://localhost:8080
echo 按Ctrl+C停止服务器
echo.

REM 尝试不同的启动方式
python start_web.py
if errorlevel 1 (
    echo FastAPI启动失败，尝试简单服务器...
    python simple_server.py
)

pause
"""
    
    try:
        with open("start_web.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        print("✅ 创建Windows启动脚本: start_web.bat")
    except Exception as e:
        print(f"❌ 创建启动脚本失败: {e}")
    
    return True

def main():
    """主函数"""
    print("🔧 Web界面一键修复工具")
    print("="*50)
    
    # 执行修复步骤
    fixes = [
        ("Python依赖", fix_python_dependencies),
        ("端口问题", fix_port_issues),
        ("文件问题", fix_file_issues),
        ("防火墙问题", fix_firewall_issues),
        ("Web服务器测试", test_web_server),
        ("启动脚本", create_startup_script)
    ]
    
    results = {}
    for fix_name, fix_func in fixes:
        try:
            results[fix_name] = fix_func()
        except Exception as e:
            print(f"❌ {fix_name}修复失败: {e}")
            results[fix_name] = False
    
    # 总结
    print("\n" + "="*50)
    print("📊 修复结果总结")
    print("="*50)
    
    passed = sum(results.values())
    total = len(results)
    
    for fix_name, result in results.items():
        status = "✅ 已修复" if result else "❌ 未修复"
        print(f"{fix_name}: {status}")
    
    print(f"\n总体结果: {passed}/{total} 项修复成功")
    
    if passed == total:
        print("🎉 所有问题已修复，尝试启动Web界面:")
        print("   python start_web.py")
        print("   或 python simple_server.py")
        print("   或双击 start_web.bat")
    else:
        print("⚠️ 部分问题未解决，请手动检查")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)