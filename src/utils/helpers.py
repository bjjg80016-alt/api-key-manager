"""
工具函数模块
提供各种辅助功能
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
import hashlib

def setup_logging(log_file: str = "logs/api_manager.log", level: str = "INFO"):
    """设置日志配置"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def load_config(config_path: str = "config/api_config.json") -> Dict[str, Any]:
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config: Dict[str, Any], config_path: str = "config/api_config.json"):
    """保存配置文件"""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def generate_key() -> str:
    """生成加密密钥"""
    return Fernet.generate_key().decode()

def encrypt_data(data: str, key: str) -> str:
    """加密数据"""
    f = Fernet(key.encode())
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str, key: str) -> str:
    """解密数据"""
    f = Fernet(key.encode())
    return f.decrypt(encrypted_data.encode()).decode()

def hash_key(key: str) -> str:
    """哈希API密钥"""
    return hashlib.sha256(key.encode()).hexdigest()

def validate_api_key(key: str) -> bool:
    """验证API密钥格式"""
    if not key:
        return False
    
    # 基本格式验证
    if len(key) < 10:
        return False
    
    # 检查是否包含常见API密钥格式
    common_patterns = ['sk-', 'pk-', 'AIza', 'ghp_', 'glpat-']
    return any(pattern in key for pattern in common_patterns)

def mask_api_key(key: str) -> str:
    """掩码API密钥"""
    if not key:
        return "***"
    
    if len(key) <= 10:
        return "*" * len(key)
    
    return f"{key[:6]}...{key[-4:]}"

def format_timestamp(timestamp: datetime) -> str:
    """格式化时间戳"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def is_key_expired(expiry_date: datetime) -> bool:
    """检查密钥是否过期"""
    return datetime.now() > expiry_date

def calculate_days_until_expiry(expiry_date: datetime) -> int:
    """计算距离过期还有多少天"""
    delta = expiry_date - datetime.now()
    return max(0, delta.days)

def create_backup(source_path: str, backup_dir: str = "backups") -> str:
    """创建备份文件"""
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(source_path)
    backup_path = os.path.join(backup_dir, f"{filename}.backup_{timestamp}")
    
    if os.path.exists(source_path):
        import shutil
        shutil.copy2(source_path, backup_path)
        return backup_path
    
    return ""

def cleanup_old_backups(backup_dir: str = "backups", days_to_keep: int = 30):
    """清理旧备份文件"""
    if not os.path.exists(backup_dir):
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_date:
                os.remove(file_path)

def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def validate_service_name(service: str) -> bool:
    """验证服务名称"""
    if not service:
        return False
    
    # 只允许字母、数字、下划线和连字符
    return service.replace('_', '').replace('-', '').isalnum()

def sanitize_service_name(service: str) -> str:
    """清理服务名称"""
    # 移除特殊字符，只保留字母、数字、下划线和连字符
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '', service)

def get_environment_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    """获取环境变量"""
    return os.getenv(key, default)

def set_environment_variable(key: str, value: str):
    """设置环境变量"""
    os.environ[key] = value

def is_docker_environment() -> bool:
    """检查是否在Docker环境中"""
    return os.path.exists('/.dockerenv') or os.getenv('DOCKERIZED') == 'true'

def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    import platform
    import psutil
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "disk_usage": psutil.disk_usage('/').total
    }