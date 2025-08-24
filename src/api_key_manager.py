#!/usr/bin/env python3
"""
API密钥管理工具
支持多种方式管理和更换API密钥
"""

import os
import json
from typing import Dict, Any, Optional

class APIKeyManager:
    def __init__(self, config_path: str = "config/api_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        default_config = {
            "api_keys": {},
            "endpoints": {},
            "rates": {}
        }
        self.save_config(default_config)
        return default_config
    
    def save_config(self, config: Dict[str, Any] = None):
        """保存配置"""
        config = config or self.config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_api_key(self, service: str) -> Optional[str]:
        """获取API密钥"""
        # 优先从环境变量获取
        env_key = f"{service.upper()}_API_KEY"
        env_value = os.getenv(env_key)
        if env_value:
            return env_value
        
        # 从配置文件获取
        return self.config.get("api_keys", {}).get(service)
    
    def set_api_key(self, service: str, key: str, save_to_file: bool = True):
        """设置API密钥"""
        if "api_keys" not in self.config:
            self.config["api_keys"] = {}
        
        self.config["api_keys"][service] = key
        
        if save_to_file:
            self.save_config()
        
        # 同时设置环境变量
        os.environ[f"{service.upper()}_API_KEY"] = key
    
    def update_api_key(self, service: str, new_key: str):
        """更新API密钥"""
        self.set_api_key(service, new_key)
        print(f"✅ {service} API密钥已更新")
    
    def remove_api_key(self, service: str):
        """删除API密钥"""
        if "api_keys" in self.config and service in self.config["api_keys"]:
            del self.config["api_keys"][service]
            self.save_config()
        
        # 删除环境变量
        env_key = f"{service.upper()}_API_KEY"
        if env_key in os.environ:
            del os.environ[env_key]
        
        print(f"❌ {service} API密钥已删除")
    
    def list_all_keys(self) -> Dict[str, str]:
        """列出所有API密钥"""
        keys = {}
        
        # 从配置文件获取
        config_keys = self.config.get("api_keys", {})
        for service, key in config_keys.items():
            keys[service] = f"{key[:10]}..." if len(key) > 10 else "***"
        
        # 从环境变量获取
        env_keys = {k: v for k, v in os.environ.items() if k.endswith("_API_KEY")}
        for env_key, value in env_keys.items():
            service = env_key.lower().replace("_api_key", "")
            keys[service] = f"{value[:10]}..." if len(value) > 10 else "***"
        
        return keys
    
    def test_api_key(self, service: str) -> bool:
        """测试API密钥是否有效"""
        key = self.get_api_key(service)
        if not key:
            print(f"❌ {service} API密钥未设置")
            return False
        
        # 这里可以添加具体的API测试逻辑
        print(f"✅ {service} API密钥已设置")
        return True
    
    def get_config_template(self) -> str:
        """获取配置模板"""
        return """
{
  "api_keys": {
    "openai": "sk-...",
    "anthropic": "sk-ant-...",
    "news_api": "your_news_api_key",
    "weather_api": "your_weather_api_key",
    "feishu": "your_feishu_webhook_url"
  },
  "endpoints": {
    "openai": "https://api.openai.com/v1",
    "anthropic": "https://api.anthropic.com",
    "news_api": "https://newsapi.org/v2",
    "weather_api": "https://api.openweathermap.org/data/2.5"
  },
  "rates": {
    "openai": {
      "rpm": 60,
      "tpm": 90000
    },
    "anthropic": {
      "rpm": 60,
      "tpm": 90000
    }
  }
}
"""

def main():
    """主函数 - 命令行界面"""
    manager = APIKeyManager()
    
    print("🔑 API密钥管理工具")
    print("=" * 40)
    
    while True:
        print("\n选项:")
        print("1. 查看所有API密钥")
        print("2. 设置/更新API密钥")
        print("3. 删除API密钥")
        print("4. 测试API密钥")
        print("5. 生成配置模板")
        print("6. 退出")
        
        choice = input("\n请选择操作 (1-6): ").strip()
        
        if choice == "1":
            keys = manager.list_all_keys()
            print("\n📋 当前API密钥:")
            for service, masked_key in keys.items():
                print(f"  {service}: {masked_key}")
        
        elif choice == "2":
            service = input("输入服务名称 (如 openai, anthropic): ").strip().lower()
            key = input("输入新的API密钥: ").strip()
            manager.update_api_key(service, key)
        
        elif choice == "3":
            service = input("输入要删除的服务名称: ").strip().lower()
            manager.remove_api_key(service)
        
        elif choice == "4":
            service = input("输入要测试的服务名称: ").strip().lower()
            manager.test_api_key(service)
        
        elif choice == "5":
            print("\n📄 配置模板:")
            print(manager.get_config_template())
        
        elif choice == "6":
            print("👋 再见!")
            break
        
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()