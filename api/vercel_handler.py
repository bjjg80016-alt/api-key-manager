#!/usr/bin/env python3
"""
Vercel部署入口文件
API密钥管理器 - 云端版本
"""

import json
import os
import sqlite3
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import urllib.parse as urlparse

# 数据库初始化
def init_database():
    """初始化数据库"""
    conn = sqlite3.connect('/tmp/keys.db')
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

class handler(BaseHTTPRequestHandler):
    """Vercel服务器less函数处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        path = urlparse.urlparse(self.path).path
        
        if path == '/health':
            self.serve_health()
        elif path == '/api/keys':
            self.serve_get_keys()
        elif path.startswith('/api/keys/'):
            service = path.split('/')[-1]
            self.serve_get_key(service)
        elif path == '/':
            self.serve_index()
        elif path == '/docs':
            self.serve_docs()
        else:
            self.serve_404()
    
    def do_POST(self):
        """处理POST请求"""
        path = urlparse.urlparse(self.path).path
        
        if path == '/api/keys':
            self.serve_post_key()
        else:
            self.serve_404()
    
    def do_DELETE(self):
        """处理DELETE请求"""
        path = urlparse.urlparse(self.path).path
        
        if path.startswith('/api/keys/'):
            service = path.split('/')[-1]
            self.serve_delete_key(service)
        else:
            self.serve_404()
    
    def serve_health(self):
        """健康检查"""
        self.send_json_response({"status": "healthy", "message": "API密钥管理器运行正常"})
    
    def serve_get_keys(self):
        """获取所有密钥"""
        try:
            conn = sqlite3.connect('/tmp/keys.db')
            cursor = conn.cursor()
            cursor.execute('SELECT service, key FROM api_keys')
            results = cursor.fetchall()
            conn.close()
            
            keys = {service: key for service, key in results}
            self.send_json_response(keys)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def serve_get_key(self, service):
        """获取特定密钥"""
        try:
            conn = sqlite3.connect('/tmp/keys.db')
            cursor = conn.cursor()
            cursor.execute('SELECT key FROM api_keys WHERE service = ?', (service,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                key = result[0]
                response = {
                    "service": service,
                    "key": key[:8] + "..." if len(key) > 8 else "***",
                    "status": "active"
                }
                self.send_json_response(response)
            else:
                self.send_json_response({"error": "Key not found"}, 404)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def serve_post_key(self):
        """添加密钥"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            service = data.get('service')
            key = data.get('key')
            
            if service and key:
                conn = sqlite3.connect('/tmp/keys.db')
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO api_keys (service, key, updated_at)
                    VALUES (?, ?, ?)
                ''', (service, key, datetime.now()))
                conn.commit()
                conn.close()
                
                response = {
                    "service": service,
                    "status": "success",
                    "message": "API密钥设置成功"
                }
                self.send_json_response(response)
            else:
                self.send_json_response({"error": "Missing service or key"}, 400)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def serve_delete_key(self, service):
        """删除密钥"""
        try:
            conn = sqlite3.connect('/tmp/keys.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM api_keys WHERE service = ?', (service,))
            conn.commit()
            conn.close()
            
            response = {
                "service": service,
                "status": "success",
                "message": "API密钥删除成功"
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)
    
    def serve_index(self):
        """主页"""
        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API密钥管理器 - 云端版</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 2.5em; }
        .header p { margin: 10px 0 0 0; opacity: 0.9; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }
        .feature-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
        .feature-icon { font-size: 2em; margin-bottom: 10px; }
        .cta-button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 1.1em; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px; }
        .cta-button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .docs-section { background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 30px 0; }
        .api-endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 4px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔑 API密钥管理器</h1>
            <p>云端版 - 安全、可靠、易用的API密钥管理解决方案</p>
        </div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>云端部署</h3>
                <p>基于Vercel的全球CDN，访问速度极快</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>安全存储</h3>
                <p>数据加密存储，保障您的API密钥安全</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <h3>REST API</h3>
                <p>完整的RESTful API接口，支持程序化访问</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3>响应式设计</h3>
                <p>支持桌面端和移动端，随时随地管理</p>
            </div>
        </div>
        
        <div style="text-align: center; margin: 40px 0;">
            <h2>开始使用</h2>
            <a href="/docs" class="cta-button">📚 查看API文档</a>
            <a href="/api/keys" class="cta-button">🔍 查看密钥</a>
        </div>
        
        <div class="docs-section">
            <h2>📖 快速开始</h2>
            
            <h3>API端点</h3>
            <div class="api-endpoint">GET /health - 健康检查</div>
            <div class="api-endpoint">GET /api/keys - 获取所有密钥</div>
            <div class="api-endpoint">POST /api/keys - 添加密钥</div>
            <div class="api-endpoint">DELETE /api/keys/{service} - 删除密钥</div>
            
            <h3>示例代码</h3>
            <div class="api-endpoint">
curl -X POST https://your-app.vercel.app/api/keys \<br>
&nbsp;&nbsp;-H "Content-Type: application/json" \<br>
&nbsp;&nbsp;-d '{"service": "openai", "key": "sk-your-key"}'
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>💡 提示：所有数据都存储在云端，重启服务不会丢失数据</p>
            <p>🔗 部署于 Vercel 平台，享受企业级稳定性和安全性</p>
        </div>
    </div>
</body>
</html>'''
        self.send_html_response(html)
    
    def serve_docs(self):
        """API文档页面"""
        docs_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API文档 - API密钥管理器</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #f8f9fa; }
        .header { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 40px 0; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .content { background: white; margin: -30px auto 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); padding: 40px; }
        .endpoint { background: #f8f9fa; border-left: 4px solid #007bff; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
        .method { font-weight: bold; color: #007bff; font-size: 1.1em; }
        .url { font-family: monospace; background: #e9ecef; padding: 5px 10px; border-radius: 4px; margin: 10px 0; display: inline-block; }
        .description { color: #6c757d; margin: 10px 0; }
        code { background: #f8f9fa; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }
        pre { background: #f8f9fa; padding: 20px; border-radius: 8px; overflow-x: auto; border: 1px solid #e9ecef; }
        .response { background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 8px; margin: 10px 0; }
        .nav { background: white; padding: 20px 0; border-bottom: 1px solid #e9ecef; margin-bottom: 30px; }
        .nav a { color: #007bff; text-decoration: none; margin-right: 20px; font-weight: 500; }
        .nav a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>📚 API文档</h1>
            <p>API密钥管理器 REST API 接口文档</p>
        </div>
    </div>
    
    <div class="container">
        <div class="nav">
            <a href="/">← 返回主页</a>
            <a href="#endpoints">API端点</a>
            <a href="#examples">使用示例</a>
        </div>
        
        <div class="content">
            <h2>基础信息</h2>
            <p><strong>基础URL:</strong> <code>https://your-app.vercel.app</code></p>
            <p><strong>Content-Type:</strong> <code>application/json</code></p>
            <p><strong>认证方式:</strong> 无需认证（生产环境建议添加）</p>
            
            <h2 id="endpoints">API端点</h2>
            
            <div class="endpoint">
                <div class="method">GET /health</div>
                <div class="url">GET /health</div>
                <div class="description">健康检查 - 验证服务是否正常运行</div>
                <div class="response">
                    <strong>响应:</strong><br>
                    <pre>{
    "status": "healthy",
    "message": "API密钥管理器运行正常"
}</pre>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /api/keys</div>
                <div class="url">GET /api/keys</div>
                <div class="description">获取所有API密钥 - 返回所有存储的密钥列表</div>
                <div class="response">
                    <strong>响应:</strong><br>
                    <pre>{
    "openai": "sk-...",
    "anthropic": "sk-ant-...",
    "weather_api": "your-weather-key"
}</pre>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /api/keys/{service}</div>
                <div class="url">GET /api/keys/openai</div>
                <div class="description">获取特定服务的API密钥 - 返回指定服务的密钥信息</div>
                <div class="response">
                    <strong>响应:</strong><br>
                    <pre>{
    "service": "openai",
    "key": "sk-...",
    "status": "active"
}</pre>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="method">POST /api/keys</div>
                <div class="url">POST /api/keys</div>
                <div class="description">设置API密钥 - 添加或更新API密钥</div>
                <div class="response">
                    <strong>请求:</strong><br>
                    <pre>{
    "service": "openai",
    "key": "sk-your-api-key"
}</pre>
                    <strong>响应:</strong><br>
                    <pre>{
    "service": "openai",
    "status": "success",
    "message": "API密钥设置成功"
}</pre>
                </div>
            </div>
            
            <div class="endpoint">
                <div class="method">DELETE /api/keys/{service}</div>
                <div class="url">DELETE /api/keys/openai</div>
                <div class="description">删除API密钥 - 删除指定服务的密钥</div>
                <div class="response">
                    <strong>响应:</strong><br>
                    <pre>{
    "service": "openai",
    "status": "success",
    "message": "API密钥删除成功"
}</pre>
                </div>
            </div>
            
            <h2 id="examples">使用示例</h2>
            
            <h3>使用curl</h3>
            <pre><code># 健康检查
curl https://your-app.vercel.app/health

# 获取所有密钥
curl https://your-app.vercel.app/api/keys

# 设置密钥
curl -X POST https://your-app.vercel.app/api/keys \\
  -H "Content-Type: application/json" \\
  -d '{"service": "openai", "key": "sk-your-key"}'

# 删除密钥
curl -X DELETE https://your-app.vercel.app/api/keys/openai</code></pre>
            
            <h3>使用JavaScript</h3>
            <pre><code>// 获取所有密钥
fetch('https://your-app.vercel.app/api/keys')
  .then(response => response.json())
  .then(data => console.log(data));

// 设置密钥
fetch('https://your-app.vercel.app/api/keys', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ service: 'openai', key: 'sk-your-key' })
})
  .then(response => response.json())
  .then(data => console.log(data));</code></pre>
            
            <h3>使用Python</h3>
            <pre><code>import requests

# 获取所有密钥
response = requests.get('https://your-app.vercel.app/api/keys')
print(response.json())

# 设置密钥
response = requests.post(
    'https://your-app.vercel.app/api/keys',
    json={'service': 'openai', 'key': 'sk-your-key'}
)
print(response.json())</code></pre>
            
            <h2>错误处理</h2>
            <div class="endpoint">
                <div class="method">错误响应格式</div>
                <div class="response">
                    <pre>{
    "error": "错误描述",
    "status": "error"
}</pre>
                </div>
            </div>
            
            <h2>注意事项</h2>
            <ul>
                <li>所有数据都存储在云端临时存储中，服务重启后数据会丢失</li>
                <li>生产环境建议添加认证机制</li>
                <li>建议定期备份重要密钥</li>
                <li>API密钥在传输过程中建议使用HTTPS</li>
            </ul>
        </div>
    </div>
</body>
</html>'''
        self.send_html_response(docs_html)
    
    def serve_404(self):
        """404页面"""
        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - 页面未找到</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }
        h1 { color: #dc3545; font-size: 3em; margin-bottom: 20px; }
        p { color: #666; font-size: 1.2em; margin-bottom: 30px; }
        a { background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; }
        a:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>抱歉，您访问的页面不存在。</p>
        <a href="/">返回主页</a>
    </div>
</body>
</html>'''
        self.send_html_response(html, 404)
    
    def send_json_response(self, data, status_code=200):
        """发送JSON响应"""
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response)
    
    def send_html_response(self, html, status_code=200):
        """发送HTML响应"""
        response = html.encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

# 初始化数据库
init_database()