// API密钥管理器前端JavaScript

class APIKeyManager {
    constructor() {
        this.baseURL = '';
        this.currentKeys = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadKeys();
    }

    bindEvents() {
        // 表单提交
        document.getElementById('keyForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveKey();
        });

        // 清空表单
        document.getElementById('clearForm').addEventListener('click', () => {
            this.clearForm();
        });

        // 刷新按钮
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadKeys();
        });

        // 测试所有密钥
        document.getElementById('testAllBtn').addEventListener('click', () => {
            this.testAllKeys();
        });

        // 配置模板
        document.getElementById('configTemplateBtn').addEventListener('click', () => {
            this.showConfigTemplate();
        });

        // 复制配置
        document.getElementById('copyConfigBtn').addEventListener('click', () => {
            this.copyConfig();
        });

        // 服务选择变化
        document.getElementById('serviceSelect').addEventListener('change', (e) => {
            this.toggleCustomService(e.target.value);
        });
    }

    toggleCustomService(service) {
        const customServiceField = document.getElementById('customService');
        if (service === 'custom') {
            customServiceField.style.display = 'block';
            customServiceField.required = true;
        } else {
            customServiceField.style.display = 'none';
            customServiceField.required = false;
            customServiceField.value = '';
        }
    }

    async loadKeys() {
        try {
            const response = await fetch(`${this.baseURL}/api/keys`);
            if (!response.ok) {
                throw new Error('加载密钥失败');
            }
            
            this.currentKeys = await response.json();
            this.renderKeys();
            this.showToast('success', '密钥列表已刷新');
        } catch (error) {
            this.showToast('error', '加载密钥失败: ' + error.message);
        }
    }

    renderKeys() {
        const keysList = document.getElementById('keysList');
        keysList.innerHTML = '';

        if (Object.keys(this.currentKeys).length === 0) {
            keysList.innerHTML = '<div class="alert alert-info">暂无API密钥</div>';
            return;
        }

        for (const [service, key] of Object.entries(this.currentKeys)) {
            const keyItem = document.createElement('div');
            keyItem.className = 'list-group-item';
            keyItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${this.getServiceDisplayName(service)}</h6>
                        <span class="key-display">${key}</span>
                    </div>
                    <div class="key-actions">
                        <span class="status-indicator status-active"></span>
                        <button class="btn btn-sm btn-outline-primary" onclick="appManager.testKey('${service}')">
                            <i class="fas fa-check"></i> 测试
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="appManager.deleteKey('${service}')">
                            <i class="fas fa-trash"></i> 删除
                        </button>
                    </div>
                </div>
            `;
            keysList.appendChild(keyItem);
        }
    }

    getServiceDisplayName(service) {
        const serviceNames = {
            'openai': 'OpenAI',
            'anthropic': 'Anthropic',
            'news_api': 'News API',
            'weather_api': 'Weather API',
            'feishu': '飞书'
        };
        return serviceNames[service] || service;
    }

    async saveKey() {
        const serviceSelect = document.getElementById('serviceSelect');
        const customService = document.getElementById('customService');
        const apiKey = document.getElementById('apiKey');

        let service = serviceSelect.value;
        if (service === 'custom') {
            service = customService.value.trim();
            if (!service) {
                this.showToast('error', '请输入自定义服务名称');
                return;
            }
        }

        if (!service || !apiKey.value) {
            this.showToast('error', '请填写完整信息');
            return;
        }

        try {
            const response = await fetch(`${this.baseURL}/api/keys`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    service: service,
                    key: apiKey.value
                })
            });

            if (!response.ok) {
                throw new Error('保存密钥失败');
            }

            this.showToast('success', '密钥保存成功');
            this.clearForm();
            this.loadKeys();
        } catch (error) {
            this.showToast('error', '保存密钥失败: ' + error.message);
        }
    }

    async deleteKey(service) {
        if (!confirm(`确定要删除 ${this.getServiceDisplayName(service)} 的密钥吗？`)) {
            return;
        }

        try {
            const response = await fetch(`${this.baseURL}/api/keys/${service}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('删除密钥失败');
            }

            this.showToast('success', '密钥删除成功');
            this.loadKeys();
        } catch (error) {
            this.showToast('error', '删除密钥失败: ' + error.message);
        }
    }

    async testKey(service) {
        try {
            const response = await fetch(`${this.baseURL}/api/keys/${service}/test`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('测试密钥失败');
            }

            const result = await response.json();
            if (result.status === 'success') {
                this.showToast('success', `${this.getServiceDisplayName(service)} 密钥测试成功`);
            } else {
                this.showToast('error', `${this.getServiceDisplayName(service)} 密钥测试失败`);
            }
        } catch (error) {
            this.showToast('error', '测试密钥失败: ' + error.message);
        }
    }

    async testAllKeys() {
        const services = Object.keys(this.currentKeys);
        if (services.length === 0) {
            this.showToast('info', '没有可测试的密钥');
            return;
        }

        this.showToast('info', '开始测试所有密钥...');

        for (const service of services) {
            await this.testKey(service);
            // 添加延迟避免请求过于频繁
            await new Promise(resolve => setTimeout(resolve, 500));
        }
    }

    async showConfigTemplate() {
        try {
            const response = await fetch(`${this.baseURL}/api/config/template`);
            if (!response.ok) {
                throw new Error('获取配置模板失败');
            }

            const data = await response.json();
            document.getElementById('configTemplate').textContent = data.template;
            
            const modal = new bootstrap.Modal(document.getElementById('configModal'));
            modal.show();
        } catch (error) {
            this.showToast('error', '获取配置模板失败: ' + error.message);
        }
    }

    copyConfig() {
        const configText = document.getElementById('configTemplate').textContent;
        navigator.clipboard.writeText(configText).then(() => {
            this.showToast('success', '配置模板已复制到剪贴板');
        }).catch(() => {
            this.showToast('error', '复制失败，请手动复制');
        });
    }

    clearForm() {
        document.getElementById('keyForm').reset();
        document.getElementById('customService').style.display = 'none';
    }

    showToast(type, message) {
        const toastEl = document.getElementById('liveToast');
        const toastTitle = document.getElementById('toastTitle');
        const toastMessage = document.getElementById('toastMessage');

        // 设置标题和消息
        const titles = {
            'success': '成功',
            'error': '错误',
            'info': '信息',
            'warning': '警告'
        };

        toastTitle.textContent = titles[type] || '通知';
        toastMessage.textContent = message;

        // 设置样式
        toastEl.className = `toast show bg-${type === 'error' ? 'danger' : type}`;
        
        // 显示toast
        const toast = new bootstrap.Toast(toastEl);
        toast.show();

        // 3秒后自动隐藏
        setTimeout(() => {
            toast.hide();
        }, 3000);
    }
}

// 初始化应用
let appManager;
document.addEventListener('DOMContentLoaded', () => {
    appManager = new APIKeyManager();
});

// 添加加载动画
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.id = 'loadingSpinner';
    document.body.appendChild(spinner);
}

function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// 添加键盘快捷键
document.addEventListener('keydown', (e) => {
    // Ctrl+R 刷新
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        appManager.loadKeys();
    }
    
    // Ctrl+S 保存
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        const form = document.getElementById('keyForm');
        if (form.checkValidity()) {
            appManager.saveKey();
        }
    }
    
    // Escape 关闭模态框
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// 添加页面可见性变化处理
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // 页面重新可见时刷新密钥列表
        appManager.loadKeys();
    }
});

// 添加网络状态监听
window.addEventListener('online', () => {
    appManager.showToast('success', '网络连接已恢复');
    appManager.loadKeys();
});

window.addEventListener('offline', () => {
    appManager.showToast('error', '网络连接已断开');
});