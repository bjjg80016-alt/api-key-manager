"""
Web界面模块
提供REST API和Web界面
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_key_manager import APIKeyManager

app = FastAPI(title="API密钥管理器", version="1.0.0")

# 静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 初始化管理器
manager = APIKeyManager()

# Pydantic模型
class APIKeyRequest(BaseModel):
    service: str
    key: str

class APIKeyResponse(BaseModel):
    service: str
    key: str
    status: str

class ServiceResponse(BaseModel):
    service: str
    status: str
    message: str

# 路由
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "API密钥管理器运行正常"}

@app.get("/api/keys", response_model=Dict[str, str])
async def get_all_keys():
    """获取所有API密钥"""
    return manager.list_all_keys()

@app.get("/api/keys/{service}", response_model=APIKeyResponse)
async def get_key(service: str):
    """获取特定服务的API密钥"""
    key = manager.get_api_key(service)
    if not key:
        raise HTTPException(status_code=404, detail=f"{service} API密钥未找到")
    
    return APIKeyResponse(
        service=service,
        key=f"{key[:10]}..." if len(key) > 10 else "***",
        status="active"
    )

@app.post("/api/keys", response_model=ServiceResponse)
async def set_key(request: APIKeyRequest):
    """设置API密钥"""
    try:
        manager.set_api_key(request.service, request.key)
        return ServiceResponse(
            service=request.service,
            status="success",
            message="API密钥设置成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/keys/{service}", response_model=ServiceResponse)
async def update_key(service: str, request: APIKeyRequest):
    """更新API密钥"""
    try:
        manager.update_api_key(service, request.key)
        return ServiceResponse(
            service=service,
            status="success",
            message="API密钥更新成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/keys/{service}", response_model=ServiceResponse)
async def delete_key(service: str):
    """删除API密钥"""
    try:
        manager.remove_api_key(service)
        return ServiceResponse(
            service=service,
            status="success",
            message="API密钥删除成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/keys/{service}/test", response_model=ServiceResponse)
async def test_key(service: str):
    """测试API密钥"""
    try:
        success = manager.test_api_key(service)
        if success:
            return ServiceResponse(
                service=service,
                status="success",
                message="API密钥测试成功"
            )
        else:
            return ServiceResponse(
                service=service,
                status="failed",
                message="API密钥测试失败"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config/template")
async def get_config_template():
    """获取配置模板"""
    return {"template": manager.get_config_template()}

@app.get("/api/services")
async def get_supported_services():
    """获取支持的服务列表"""
    return {
        "services": [
            {"name": "openai", "description": "OpenAI API"},
            {"name": "anthropic", "description": "Anthropic Claude API"},
            {"name": "news_api", "description": "News API"},
            {"name": "weather_api", "description": "OpenWeatherMap API"},
            {"name": "feishu", "description": "飞书Webhook"}
        ]
    }

def create_app():
    """创建FastAPI应用"""
    return app

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="API密钥管理器Web界面")
    parser.add_argument("--host", default="127.0.0.1", help="主机地址")
    parser.add_argument("--port", type=int, default=8080, help="端口号")
    parser.add_argument("--dev", action="store_true", help="开发模式")
    
    args = parser.parse_args()
    
    print(f"🚀 启动API密钥管理器Web界面")
    print(f"📍 地址: http://{args.host}:{args.port}")
    print(f"📖 API文档: http://{args.host}:{args.port}/docs")
    
    uvicorn.run(
        "web_interface:app",
        host=args.host,
        port=args.port,
        reload=args.dev,
        log_level="info"
    )

if __name__ == "__main__":
    main()