// 修复后的Supabase配置
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
