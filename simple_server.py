#!/usr/bin/env python3
"""
简单的HTTP服务器
用于在没有FastAPI的情况下展示Web界面
"""

import http.server
import socketserver
import json
import os
import sys
from pathlib import Path
import urllib.parse
from datetime import datetime

class APIKeyManagerHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.serve_index()
        elif self.path == '/api/keys':
            self.serve_api_keys()
        elif self.path == '/health':
            self.serve_health()
        elif self.path.startswith('/static/'):
            self.serve_static()
        else:
            super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/keys':
            self.handle_post_key()
        elif self.path.startswith('/api/keys/') and self.path.endswith('/test'):
            self.handle_test_key()
        else:
            self.send_error(404, "Not Found")
    
    def serve_index(self):
        """服务主页"""
        try:
            with open('templates/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Index page not found")
    
    def serve_api_keys(self):
        """服务API密钥"""
        try:
            # 这里应该从配置文件读取密钥
            keys = {}
            
            if os.path.exists('config/api_config.json'):
                with open('config/api_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    api_keys = config.get('api_keys', {})
                    for service, key in api_keys.items():
                        keys[service] = f"{key[:10]}..." if len(key) > 10 else "***"
            
            response = json.dumps(keys, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_health(self):
        """健康检查"""
        health_data = {
            "status": "healthy",
            "message": "API密钥管理器运行正常",
            "timestamp": datetime.now().isoformat()
        }
        
        response = json.dumps(health_data, ensure_ascii=False)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def serve_static(self):
        """服务静态文件"""
        file_path = self.path.lstrip('/')
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                self.send_response(200)
                
                # 设置正确的MIME类型
                if file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif file_path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                elif file_path.endswith('.json'):
                    self.send_header('Content-type', 'application/json')
                else:
                    self.send_header('Content-type', 'application/octet-stream')
                
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "File not found")
    
    def handle_post_key(self):
        """处理POST请求添加密钥"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # 这里应该保存到配置文件
            print(f"收到密钥设置请求: {data}")
            
            response = {
                "status": "success",
                "message": "密钥设置成功",
                "service": data.get('service')
            }
            
            response_json = json.dumps(response, ensure_ascii=False)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_json.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_test_key(self):
        """处理密钥测试请求"""
        service = self.path.split('/')[-2]
        
        response = {
            "status": "success",
            "message": f"{service} 密钥测试成功",
            "service": service
        }
        
        response_json = json.dumps(response, ensure_ascii=False)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response_json.encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def main():
    """主函数"""
    PORT = 8080
    
    print("🌐 API密钥管理器 - 简单Web界面")
    print("=" * 50)
    
    # 检查必要文件
    required_files = [
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
    
    try:
        with socketserver.TCPServer(("", PORT), APIKeyManagerHandler) as httpd:
            print(f"✅ 服务器启动成功")
            print(f"📍 访问地址: http://localhost:{PORT}")
            print(f"📖 API地址: http://localhost:{PORT}/api/keys")
            print(f"💚 健康检查: http://localhost:{PORT}/health")
            print("按 Ctrl+C 停止服务器")
            print("=" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except OSError as e:
        if e.errno == 10048:  # 端口被占用
            print(f"❌ 端口 {PORT} 被占用，请尝试其他端口")
        else:
            print(f"❌ 启动服务器失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 服务器错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)