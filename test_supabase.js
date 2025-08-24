// 测试Supabase连接
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
