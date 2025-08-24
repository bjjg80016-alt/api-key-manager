#!/bin/bash

# API密钥管理工具部署脚本
# 使用方法: ./deploy.sh [dev|prod]

set -e

ENVIRONMENT=${1:-dev}
PROJECT_ROOT=$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")
cd "$PROJECT_ROOT"

echo "🎬 开始部署API密钥管理工具..."
echo "环境: $ENVIRONMENT"
echo "项目目录: $PROJECT_ROOT"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Python
check_python() {
    log_info "检查Python环境..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    log_info "Python版本: $PYTHON_VERSION"
}

# 创建虚拟环境
create_venv() {
    log_info "创建虚拟环境..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_info "虚拟环境创建成功"
    else
        log_info "虚拟环境已存在"
    fi
    
    source venv/bin/activate
    log_info "激活虚拟环境"
}

# 安装依赖
install_deps() {
    log_info "安装依赖..."
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        log_info "依赖安装完成"
    else
        log_error "requirements.txt 不存在"
        exit 1
    fi
}

# 创建目录
create_dirs() {
    log_info "创建目录结构..."
    
    mkdir -p logs config data backups static templates
    
    log_info "目录创建完成"
}

# 设置配置
setup_config() {
    log_info "设置配置..."
    
    if [ ! -f "config/api_config.json" ]; then
        log_error "配置文件不存在: config/api_config.json"
        exit 1
    fi
    
    # 复制环境配置
    if [ "$ENVIRONMENT" = "prod" ]; then
        cp config/api_config.json config/api_config.json.bak
        log_info "生产环境配置已备份"
    fi
    
    log_info "配置设置完成"
}

# 运行测试
run_tests() {
    log_info "运行测试..."
    
    if [ -d "tests" ]; then
        python -m pytest tests/ -v
        log_info "测试完成"
    else
        log_warn "测试目录不存在，跳过测试"
    fi
}

# 启动服务
start_service() {
    log_info "启动服务..."
    
    if [ "$ENVIRONMENT" = "dev" ]; then
        log_info "开发环境启动..."
        python src/web_interface.py --dev
    else
        log_info "生产环境启动..."
        nohup python src/web_interface.py > logs/app.log 2>&1 &
        echo $! > logs/app.pid
        log_info "服务已启动，PID: $(cat logs/app.pid)"
    fi
}

# 主函数
main() {
    log_info "开始部署流程..."
    
    check_python
    create_venv
    install_deps
    create_dirs
    setup_config
    run_tests
    
    log_info "部署完成！"
    
    # 询问是否启动服务
    read -p "是否启动服务? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_service
    fi
    
    log_info "部署脚本执行完成"
}

# 错误处理
trap 'log_error "部署过程中发生错误"' ERR

# 执行主函数
main "$@"