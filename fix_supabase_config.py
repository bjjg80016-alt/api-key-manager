#!/usr/bin/env python3
"""
Supabase配置修复脚本
解决注册失败问题
"""

import json
import os

def fix_supabase_config():
    """修复Supabase配置文件"""
    
    print("🔧 开始修复Supabase配置...")
    
    # 1. 检查当前配置
    config_file = "supabase_config.js"
    if os.path.exists(config_file):
        print(f"✅ 找到配置文件: {config_file}")
        
        # 读取当前配置
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否使用了service_role密钥
        if "service_role" in content:
            print("❌ 检测到使用了service_role密钥")
            print("⚠️  客户端应该使用anon密钥")
            
            # 提示用户获取正确的密钥
            print("\n📋 请按照以下步骤获取正确的密钥：")
            print("1. 访问: https://supabase.com/dashboard/project/hueetdgvehilpgzbwzjhe")
            print("2. 进入 Settings → API")
            print("3. 复制 'anon public' 密钥")
            print("4. 替换supabase_config.js中的密钥")
            
        else:
            print("✅ 密钥配置看起来正确")
    
    # 2. 检查数据库表
    print("\n📊 检查数据库表...")
    print("请确保已运行以下SQL脚本：")
    
    sql_script = """
    -- 创建用户表
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- 创建API密钥表
    CREATE TABLE IF NOT EXISTS api_keys (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES users(id),
        service TEXT NOT NULL,
        key TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- 创建代理日志表
    CREATE TABLE IF NOT EXISTS agent_logs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES users(id),
        agent TEXT NOT NULL,
        action TEXT NOT NULL,
        details JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    
    print(sql_script)
    
    # 3. 创建修复后的配置文件
    print("\n🔧 创建修复后的配置文件...")
    
    fixed_config = '''// 修复后的Supabase配置
const supabaseUrl = 'https://hueetdgvehilpgzbwzjhe.supabase.co'
// 请替换为您的anon密钥
const supabaseKey = 'YOUR_ANON_KEY_HERE'

// 创建Supabase客户端
const supabase = window.supabase.createClient(supabaseUrl, supabaseKey)

// 导出配置
window.supabaseConfig = {
    url: supabaseUrl,
    key: supabaseKey,
    client: supabase
}
'''
    
    with open("supabase_config_fixed.js", 'w', encoding='utf-8') as f:
        f.write(fixed_config)
    
    print("✅ 已创建修复后的配置文件: supabase_config_fixed.js")
    
    # 4. 创建测试脚本
    print("\n🧪 创建测试脚本...")
    
    test_script = '''// 测试Supabase连接
async function testSupabaseConnection() {
    try {
        console.log("正在测试Supabase连接...")
        
        const { data, error } = await supabase
            .from('api_keys')
            .select('count')
            .limit(1)
        
        if (error) {
            console.error("连接失败:", error.message)
            return false
        } else {
            console.log("连接成功!")
            return true
        }
    } catch (err) {
        console.error("连接异常:", err.message)
        return false
    }
}

// 测试用户注册
async function testUserRegistration() {
    try {
        console.log("正在测试用户注册...")
        
        const { data, error } = await supabase.auth.signUp({
            email: 'test@example.com',
            password: 'testpassword123'
        })
        
        if (error) {
            console.error("注册失败:", error.message)
            return false
        } else {
            console.log("注册成功!")
            return true
        }
    } catch (err) {
        console.error("注册异常:", err.message)
        return false
    }
}

// 运行测试
testSupabaseConnection().then(success => {
    if (success) {
        testUserRegistration()
    }
})
'''
    
    with open("test_supabase.js", 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ 已创建测试脚本: test_supabase.js")
    
    # 5. 总结
    print("\n🎯 修复总结:")
    print("1. ✅ 检查了当前配置")
    print("2. ✅ 提供了正确的SQL脚本")
    print("3. ✅ 创建了修复后的配置文件")
    print("4. ✅ 创建了测试脚本")
    print("\n📋 下一步操作:")
    print("1. 获取正确的anon密钥")
    print("2. 更新supabase_config_fixed.js中的密钥")
    print("3. 在Supabase中运行SQL脚本")
    print("4. 测试连接和注册功能")

if __name__ == "__main__":
    fix_supabase_config()
