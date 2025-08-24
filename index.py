#!/usr/bin/env python3
"""
Vercel部署入口文件 - 简化版
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
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; margin: 0; font-size: 2.5em; }
        .header p { color: #666; margin: 10px 0 0 0; }
        .api-test { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 25px; border: none; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; margin: 5px; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .status { padding: 15px; border-radius: 8px; margin: 15px 0; }
        .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .code { background: #f8f9fa; padding: 15px; border-radius: 8px; font-family: monospace; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔑 API密钥管理器</h1>
            <p>云端版 - 已成功部署到Vercel</p>
        </div>
        
        <div class="status success">
            <strong>✅ 部署状态：</strong>服务运行正常
        </div>
        
        <div class="api-test">
            <h3>🧪 测试API接口</h3>
            <button class="btn" onclick="testHealth()">测试健康检查</button>
            <button class="btn" onclick="testKeys()">测试密钥接口</button>
            <button class="btn" onclick="addTestKey()">添加测试密钥</button>
            <div id="test-result"></div>
        </div>
        
        <div class="status info">
            <h3>📖 API端点</h3>
            <div class="code">GET /health - 健康检查</div>
            <div class="code">GET /api/keys - 获取所有密钥</div>
            <div class="code">POST /api/keys - 添加密钥</div>
            <div class="code">DELETE /api/keys/{service} - 删除密钥</div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/docs" class="btn">📚 查看完整文档</a>
            <a href="/api/keys" class="btn">🔍 查看当前密钥</a>
        </div>
        
        <div style="margin-top: 30px; text-align: center; color: #666;">
            <p>💡 部署于 Vercel 平台 | 🌍 全球CDN加速 | 🔒 自动HTTPS</p>
        </div>
    </div>
    
    <script>
        async function testHealth() {
            try {
                const response = await fetch('/health');
                const data = await response.json();
                document.getElementById('test-result').innerHTML = 
                    `<div class="status success">健康检查: ${data.status} - ${data.message}</div>`;
            } catch (error) {
                document.getElementById('test-result').innerHTML = 
                    `<div class="status" style="background: #f8d7da; color: #721c24;">健康检查失败: ${error.message}</div>`;
            }
        }
        
        async function testKeys() {
            try {
                const response = await fetch('/api/keys');
                const data = await response.json();
                document.getElementById('test-result').innerHTML = 
                    `<div class="status success">当前密钥: ${Object.keys(data).length} 个<br>${JSON.stringify(data, null, 2)}</div>`;
            } catch (error) {
                document.getElementById('test-result').innerHTML = 
                    `<div class="status" style="background: #f8d7da; color: #721c24;">获取密钥失败: ${error.message}</div>`;
            }
        }
        
        async function addTestKey() {
            try {
                const response = await fetch('/api/keys', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service: 'test', key: 'test123' })
                });
                const data = await response.json();
                document.getElementById('test-result').innerHTML = 
                    `<div class="status success">添加测试密钥: ${data.message}</div>`;
            } catch (error) {
                document.getElementById('test-result').innerHTML = 
                    `<div class="status" style="background: #f8d7da; color: #721c24;">添加密钥失败: ${error.message}</div>`;
            }
        }
    </script>
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
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f8f9fa; }
        .header { background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 40px 0; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .content { background: white; margin: -30px auto 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); padding: 40px; }
        .endpoint { background: #f8f9fa; border-left: 4px solid #007bff; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0; }
        .method { font-weight: bold; color: #007bff; font-size: 1.1em; }
        .url { font-family: monospace; background: #e9ecef; padding: 5px 10px; border-radius: 4px; margin: 10px 0; display: inline-block; }
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
        </div>
        
        <div class="content">
            <h2>API端点</h2>
            
            <div class="endpoint">
                <div class="method">GET /health</div>
                <div class="url">GET /health</div>
                <p>健康检查 - 验证服务是否正常运行</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET /api/keys</div>
                <div class="url">GET /api/keys</div>
                <p>获取所有API密钥 - 返回所有存储的密钥列表</p>
            </div>
            
            <div class="endpoint">
                <div class="method">POST /api/keys</div>
                <div class="url">POST /api/keys</div>
                <p>设置API密钥 - 添加或更新API密钥</p>
            </div>
            
            <div class="endpoint">
                <div class="method">DELETE /api/keys/{service}</div>
                <div class="url">DELETE /api/keys/openai</div>
                <p>删除API密钥 - 删除指定服务的密钥</p>
            </div>
            
            <h2>使用示例</h2>
            <pre><code># 获取所有密钥
curl https://your-app.vercel.app/api/keys

# 添加密钥
curl -X POST https://your-app.vercel.app/api/keys \\
  -H "Content-Type: application/json" \\
  -d '{"service": "openai", "key": "sk-your-key"}'</code></pre>
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
    <title>404 - 页面未找到</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }
        h1 { color: #dc3545; font-size: 3em; margin-bottom: 20px; }
        a { background: #007bff; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; }
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