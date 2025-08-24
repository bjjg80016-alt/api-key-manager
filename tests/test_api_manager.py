"""
API密钥管理工具测试套件
"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
import sys

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_key_manager import APIKeyManager
from utils.helpers import (
    setup_logging, 
    load_config, 
    save_config, 
    encrypt_data, 
    decrypt_data,
    mask_api_key,
    validate_api_key,
    is_docker_environment
)

class TestAPIKeyManager:
    """测试API密钥管理器核心功能"""
    
    def setup_method(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        self.manager = APIKeyManager(self.config_path)
    
    def teardown_method(self):
        """测试后清理"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_init_with_existing_config(self):
        """测试使用现有配置文件初始化"""
        test_config = {
            "api_keys": {"test_service": "test_key"},
            "endpoints": {"test_service": "https://api.test.com"}
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
        
        manager = APIKeyManager(self.config_path)
        assert manager.config == test_config
    
    def test_init_without_config(self):
        """测试没有配置文件时的初始化"""
        manager = APIKeyManager(self.config_path)
        assert "api_keys" in manager.config
        assert "endpoints" in manager.config
        assert "rates" in manager.config
    
    def test_set_and_get_api_key(self):
        """测试设置和获取API密钥"""
        service = "test_service"
        key = "test_api_key_12345"
        
        self.manager.set_api_key(service, key)
        retrieved_key = self.manager.get_api_key(service)
        
        assert retrieved_key == key
    
    def test_get_api_key_from_env(self):
        """测试从环境变量获取API密钥"""
        service = "test_service"
        key = "env_api_key_12345"
        
        with patch.dict(os.environ, {f"{service.upper()}_API_KEY": key}):
            retrieved_key = self.manager.get_api_key(service)
            assert retrieved_key == key
    
    def test_update_api_key(self):
        """测试更新API密钥"""
        service = "test_service"
        old_key = "old_key_123"
        new_key = "new_key_456"
        
        self.manager.set_api_key(service, old_key)
        self.manager.update_api_key(service, new_key)
        
        retrieved_key = self.manager.get_api_key(service)
        assert retrieved_key == new_key
    
    def test_remove_api_key(self):
        """测试删除API密钥"""
        service = "test_service"
        key = "test_key_12345"
        
        self.manager.set_api_key(service, key)
        self.manager.remove_api_key(service)
        
        retrieved_key = self.manager.get_api_key(service)
        assert retrieved_key is None
    
    def test_list_all_keys(self):
        """测试列出所有API密钥"""
        services = ["service1", "service2", "service3"]
        keys = ["key1", "key2", "key3"]
        
        for service, key in zip(services, keys):
            self.manager.set_api_key(service, key)
        
        all_keys = self.manager.list_all_keys()
        
        assert len(all_keys) == 3
        for service in services:
            assert service in all_keys
            assert all_keys[service].endswith("...")
    
    def test_test_api_key(self):
        """测试API密钥验证"""
        service = "test_service"
        key = "test_key_12345"
        
        self.manager.set_api_key(service, key)
        result = self.manager.test_api_key(service)
        
        assert result is True
    
    def test_test_api_key_not_set(self):
        """测试未设置的API密钥验证"""
        service = "nonexistent_service"
        result = self.manager.test_api_key(service)
        
        assert result is False
    
    def test_get_config_template(self):
        """测试获取配置模板"""
        template = self.manager.get_config_template()
        
        assert isinstance(template, str)
        assert "api_keys" in template
        assert "endpoints" in template
        assert "rates" in template

class TestHelpers:
    """测试工具函数"""
    
    def test_setup_logging(self):
        """测试日志设置"""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, 'test.log')
            logger = setup_logging(log_file)
            
            assert logger is not None
            assert os.path.exists(log_file)
    
    def test_load_and_save_config(self):
        """测试配置文件加载和保存"""
        test_config = {"test": "value"}
        
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, 'test_config.json')
            
            save_config(test_config, config_path)
            loaded_config = load_config(config_path)
            
            assert loaded_config == test_config
    
    def test_encrypt_and_decrypt_data(self):
        """测试数据加密和解密"""
        key = "test_encryption_key_123"
        data = "sensitive_data_12345"
        
        encrypted = encrypt_data(data, key)
        decrypted = decrypt_data(encrypted, key)
        
        assert decrypted == data
        assert encrypted != data
    
    def test_mask_api_key(self):
        """测试API密钥掩码"""
        # 短密钥
        short_key = "short"
        masked = mask_api_key(short_key)
        assert masked == "*****"
        
        # 长密钥
        long_key = "very_long_api_key_123456789"
        masked = mask_api_key(long_key)
        assert masked.startswith("very_l")
        assert masked.endswith("6789")
        assert "..." in masked
    
    def test_validate_api_key(self):
        """测试API密钥验证"""
        # 有效密钥格式
        valid_keys = [
            "sk-1234567890abcdef",
            "pk-1234567890abcdef",
            "AIzaSyC1234567890",
            "ghp_1234567890abcdef",
            "glpat-1234567890abcdef"
        ]
        
        for key in valid_keys:
            assert validate_api_key(key) is True
        
        # 无效密钥格式
        invalid_keys = [
            "",
            "short",
            "invalid_key_format",
            None
        ]
        
        for key in invalid_keys:
            assert validate_api_key(key) is False
    
    def test_is_docker_environment(self):
        """测试Docker环境检测"""
        # 模拟Docker环境
        with patch('os.path.exists', return_value=True):
            assert is_docker_environment() is True
        
        # 模拟非Docker环境
        with patch('os.path.exists', return_value=False):
            with patch.dict(os.environ, {}, clear):
                assert is_docker_environment() is False

class TestWebInterface:
    """测试Web界面"""
    
    def setup_method(self):
        """测试前设置"""
        # 导入Web界面模块
        from web_interface import app
        
        self.app = app
        self.client = app.test_client()
    
    def test_health_check(self):
        """测试健康检查端点"""
        response = self.client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_get_all_keys(self):
        """测试获取所有密钥端点"""
        response = self.client.get('/api/keys')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_get_supported_services(self):
        """测试获取支持的服务列表"""
        response = self.client.get('/api/services')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'services' in data
        assert len(data['services']) > 0
    
    def test_get_config_template(self):
        """测试获取配置模板"""
        response = self.client.get('/api/config/template')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'template' in data
        assert isinstance(data['template'], str)

class TestIntegration:
    """集成测试"""
    
    def setup_method(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'test_config.json')
        self.manager = APIKeyManager(self.config_path)
    
    def teardown_method(self):
        """测试后清理"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_complete_workflow(self):
        """测试完整工作流程"""
        # 1. 设置多个API密钥
        services = ["openai", "anthropic", "news_api"]
        keys = ["sk-openai-123", "sk-anthropic-456", "news-key-789"]
        
        for service, key in zip(services, keys):
            self.manager.set_api_key(service, key)
        
        # 2. 验证所有密钥都已设置
        all_keys = self.manager.list_all_keys()
        assert len(all_keys) == 3
        
        for service in services:
            assert service in all_keys
        
        # 3. 测试所有密钥
        for service in services:
            result = self.manager.test_api_key(service)
            assert result is True
        
        # 4. 更新一个密钥
        self.manager.update_api_key("openai", "sk-openai-updated")
        updated_key = self.manager.get_api_key("openai")
        assert updated_key == "sk-openai-updated"
        
        # 5. 删除一个密钥
        self.manager.remove_api_key("news_api")
        deleted_key = self.manager.get_api_key("news_api")
        assert deleted_key is None
        
        # 6. 验证最终状态
        final_keys = self.manager.list_all_keys()
        assert len(final_keys) == 2
        assert "openai" in final_keys
        assert "anthropic" in final_keys
        assert "news_api" not in final_keys

if __name__ == "__main__":
    pytest.main([__file__, "-v"])