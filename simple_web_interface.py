#!/usr/bin/env python3
"""
简化版Web界面 - 使用Flask
无需额外依赖，使用Python标准库
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sqlite3
import base64
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class APIKeyManager:
    """简化版API密钥管理器"""
    
    def __init__(self):
        self.config_file = "config/api_config.json"
        self.db_file = "data/keys.db"
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT UNIQUE NOT NULL,
                key TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def set_api_key(self, service, key):
        """设置API密钥"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO api_keys (service, key, updated_at)
            VALUES (?, ?, ?)
        ''', (service, key, datetime.now()))
        conn.commit()
        conn.close()
    
    def get_api_key(self, service):
        """获取API密钥"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT key FROM api_keys WHERE service = ?', (service,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def list_all_keys(self):
        """列出所有密钥"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT service, key FROM api_keys')
        results = cursor.fetchall()
        conn.close()
        return {service: key for service, key in results}
    
    def remove_api_key(self, service):
        """删除API密钥"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM api_keys WHERE service = ?', (service,))
        conn.commit()
        conn.close()

class WebInterfaceHandler(SimpleHTTPRequestHandler):
    """自定义Web界面处理器"""
    
    def __init__(self, *args, **kwargs):
        self.manager = APIKeyManager()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_index()
        elif self.path == '/docs':
            self.serve_docs()
        elif self.path == '/health':
            self.serve_health()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def serve_index(self):
        """提供主页"""
        html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API密钥管理器</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .key-list { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
        .key-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #ddd; }
        .key-item:last-child { border-bottom: none; }
        .btn-delete { background: #dc3545; }
        .btn-delete:hover { background: #c82333; }
        .message { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔑 API密钥管理器</h1>
            <p>管理您的API密钥</p>
        </div>
        
        <div id="message"></div>
        
        <div class="key-list">
            <h3>当前密钥</h3>
            <div id="keysList">
                <!-- 密钥列表将在这里显示 -->
            </div>
        </div>
        
        <div class="form-group">
            <h3>添加/编辑密钥</h3>
            <form id="keyForm">
                <div class="form-group">
                    <label for="service">服务名称:</label>
                    <select id="service" required>
                        <option value="">选择服务...</option>
                        <option value="openai">OpenAI</option>
                        <option value="anthropic">Anthropic</option>
                        <option value="news_api">News API</option>
                        <option value="weather_api">Weather API</option>
                        <option value="feishu">飞书</option>
                        <option value="custom">自定义</option>
                    </select>
                </div>
                
                <div class="form-group" id="customServiceGroup" style="display: none;">
                    <label for="customService">自定义服务名称:</label>
                    <input type="text" id="customService" placeholder="输入服务名称">
                </div>
                
                <div class="form-group">
                    <label for="apiKey">API密钥:</label>
                    <input type="password" id="apiKey" placeholder="输入API密钥" required>
                </div>
                
                <button type="submit">保存密钥</button>
                <button type="button" onclick="clearForm()">清空</button>
            </form>
        </div>
        
        <div class="form-group">
            <button onclick="loadKeys()">刷新</button>
            <button onclick="window.open('/docs', '_blank')">API文档</button>
        </div>
    </div>
    
    <script>
        // 显示消息
        function showMessage(text, type = 'success') {
            const messageDiv = document.getElementById('message');
            messageDiv.innerHTML = `<div class="message ${type}">${text}</div>`;
            setTimeout(() => messageDiv.innerHTML = '', 3000);
        }
        
        // 加载密钥列表
        async function loadKeys() {
            try {
                const response = await fetch('/api/keys');
                const keys = await response.json();
                
                const keysList = document.getElementById('keysList');
                keysList.innerHTML = '';
                
                for (const [service, key] of Object.entries(keys)) {
                    const maskedKey = key.substring(0, 8) + '...';
                    keysList.innerHTML += `
                        <div class="key-item">
                            <span><strong>${service}:</strong> ${maskedKey}</span>
                            <button class="btn-delete" onclick="deleteKey('${service}')">删除</button>
                        </div>
                    `;
                }
                
                if (Object.keys(keys).length === 0) {
                    keysList.innerHTML = '<p>暂无密钥</p>';
                }
            } catch (error) {
                showMessage('加载密钥失败: ' + error.message, 'error');
            }
        }
        
        // 保存密钥
        async function saveKey() {
            const serviceSelect = document.getElementById('service');
            const customService = document.getElementById('customService');
            const apiKey = document.getElementById('apiKey');
            
            let service = serviceSelect.value;
            if (service === 'custom') {
                service = customService.value;
                if (!service) {
                    showMessage('请输入自定义服务名称', 'error');
                    return;
                }
            }
            
            if (!service || !apiKey.value) {
                showMessage('请填写完整信息', 'error');
                return;
            }
            
            try {
                const response = await fetch('/api/keys', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service, key: apiKey.value })
                });
                
                const result = await response.json();
                if (result.status === 'success') {
                    showMessage(result.message);
                    clearForm();
                    loadKeys();
                } else {
                    showMessage(result.message || '保存失败', 'error');
                }
            } catch (error) {
                showMessage('保存失败: ' + error.message, 'error');
            }
        }
        
        // 删除密钥
        async function deleteKey(service) {
            if (!confirm(`确定要删除 ${service} 的密钥吗？`)) {
                return;
            }
            
            try {
                const response = await fetch(`/api/keys/${service}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                if (result.status === 'success') {
                    showMessage(result.message);
                    loadKeys();
                } else {
                    showMessage(result.message || '删除失败', 'error');
                }
            } catch (error) {
                showMessage('删除失败: ' + error.message, 'error');
            }
        }
        
        // 清空表单
        function clearForm() {
            document.getElementById('keyForm').reset();
            document.getElementById('customServiceGroup').style.display = 'none';
        }
        
        // 监听服务选择变化
        document.getElementById('service').addEventListener('change', function() {
            const customGroup = document.getElementById('customServiceGroup');
            customGroup.style.display = this.value === 'custom' ? 'block' : 'none';
        });
        
        // 监听表单提交
        document.getElementById('keyForm').addEventListener('submit', function(e) {
            e.preventDefault();
            saveKey();
        });
        
        // 页面加载时初始化
        window.onload = function() {
            loadKeys();
        };
    </script>
</body>
</html>
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_docs(self):
        """提供API文档"""
        docs_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API文档 - API密钥管理器</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { background: #28a745; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #007bff; }
        .method { font-weight: bold; color: #007bff; }
        .description { color: #666; margin: 5px 0; }
        code { background: #e9ecef; padding: 2px 4px; border-radius: 3px; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 API文档</h1>
            <p>API密钥管理器 REST API 接口文档</p>
        </div>
        
        <h2>基础信息</h2>
        <p><strong>基础URL:</strong> <code>http://localhost:8080</code></p>
        <p><strong>Content-Type:</strong> <code>application/json</code></p>
        
        <h2>API端点</h2>
        
        <div class="endpoint">
            <div class="method">GET /health</div>
            <div class="description">健康检查</div>
            <pre><code>响应:
{
    "status": "healthy",
    "message": "API密钥管理器运行正常"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <div class="method">GET /api/keys</div>
            <div class="description">获取所有API密钥</div>
            <pre><code>响应:
{
    "openai": "sk-...",
    "anthropic": "sk-ant-..."
}</code></pre>
        </div>
        
        <div class="endpoint">
            <div class="method">GET /api/keys/{service}</div>
            <div class="description">获取特定服务的API密钥</div>
            <pre><code>响应:
{
    "service": "openai",
    "key": "sk-...",
    "status": "active"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <div class="method">POST /api/keys</div>
            <div class="description">设置API密钥</div>
            <pre><code>请求:
{
    "service": "openai",
    "key": "sk-your-api-key"
}

响应:
{
    "service": "openai",
    "status": "success",
    "message": "API密钥设置成功"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <div class="method">DELETE /api/keys/{service}</div>
            <div class="description">删除API密钥</div>
            <pre><code>响应:
{
    "service": "openai",
    "status": "success",
    "message": "API密钥删除成功"
}</code></pre>
        </div>
        
        <h2>使用示例</h2>
        
        <h3>使用curl</h3>
        <pre><code># 获取所有密钥
curl http://localhost:8080/api/keys

# 设置密钥
curl -X POST http://localhost:8080/api/keys \\
  -H "Content-Type: application/json" \\
  -d '{"service": "openai", "key": "sk-your-key"}'

# 删除密钥
curl -X DELETE http://localhost:8080/api/keys/openai</code></pre>
        
        <h3>使用JavaScript</h3>
        <pre><code>// 获取所有密钥
fetch('/api/keys')
  .then(response => response.json())
  .then(data => console.log(data));

// 设置密钥
fetch('/api/keys', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ service: 'openai', key: 'sk-your-key' })
})
  .then(response => response.json())
  .then(data => console.log(data));</code></pre>
        
        <div style="margin-top: 30px; text-align: center;">
            <a href="/" style="color: #007bff; text-decoration: none;">← 返回主页</a>
        </div>
    </div>
</body>
</html>
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(docs_html.encode('utf-8'))
    
    def serve_health(self):
        """健康检查"""
        response = {"status": "healthy", "message": "API密钥管理器运行正常"}
        self.send_json_response(response)
    
    def handle_api_get(self):
        """处理API GET请求"""
        try:
            if self.path == '/api/keys':
                keys = self.manager.list_all_keys()
                self.send_json_response(keys)
            elif self.path.startswith('/api/keys/'):
                service = self.path.split('/')[-1]
                key = self.manager.get_api_key(service)
                if key:
                    response = {
                        "service": service,
                        "key": key[:8] + "..." if len(key) > 8 else "***",
                        "status": "active"
                    }
                    self.send_json_response(response)
                else:
                    self.send_json_response({"error": "Key not found"}, 404)
            else:
                self.send_error(404)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def handle_api_post(self):
        """处理API POST请求"""
        try:
            if self.path == '/api/keys':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                service = data.get('service')
                key = data.get('key')
                
                if service and key:
                    self.manager.set_api_key(service, key)
                    response = {
                        "service": service,
                        "status": "success",
                        "message": "API密钥设置成功"
                    }
                    self.send_json_response(response)
                else:
                    self.send_json_response({"error": "Missing service or key"}, 400)
            else:
                self.send_error(404)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def do_DELETE(self):
        """处理DELETE请求"""
        try:
            if self.path.startswith('/api/keys/'):
                service = self.path.split('/')[-1]
                self.manager.remove_api_key(service)
                response = {
                    "service": service,
                    "status": "success",
                    "message": "API密钥删除成功"
                }
                self.send_json_response(response)
            else:
                self.send_error(404)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def send_json_response(self, data, status_code=200):
        """发送JSON响应"""
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        """自定义日志消息"""
        print(f"[{self.address_string()}] {format % args}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="简化版API密钥管理器")
    parser.add_argument("--host", default="127.0.0.1", help="主机地址")
    parser.add_argument("--port", type=int, default=8080, help="端口号")
    
    args = parser.parse_args()
    
    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("backups", exist_ok=True)
    
    print("启动简化版API密钥管理器")
    print(f"地址: http://{args.host}:{args.port}")
    print(f"API文档: http://{args.host}:{args.port}/docs")
    print(f"健康检查: http://{args.host}:{args.port}/health")
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    
    server = HTTPServer((args.host, args.port), WebInterfaceHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.shutdown()

if __name__ == "__main__":
    main()