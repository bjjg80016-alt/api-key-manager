// Supabase配置文件
import { createClient } from '@supabase/supabase-js'

// Supabase配置
const supabaseUrl = 'https://hueetdgvehilpgzbwzjhe.supabase.co'
const supabaseKey = process.env.SUPABASE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1ZXRkZ3ZlaGlscGd6Ynd6anhlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjA0MTA3NCwiZXhwIjoyMDcxNjE3MDc0fQ.p7WEGWTj9SvebbbUSCp_j476I4aeE5UjwQQT1Q9LXOk'

// 创建Supabase客户端
const supabase = createClient(supabaseUrl, supabaseKey)

// 数据库表结构定义
export const TABLES = {
  USERS: 'users',
  API_KEYS: 'api_keys',
  AGENT_LOGS: 'agent_logs',
  USER_PREFERENCES: 'user_preferences',
  NEWS_ARTICLES: 'news_articles',
  WEATHER_DATA: 'weather_data',
  HEALTH_RECORDS: 'health_records',
  TASKS: 'tasks',
  REFLECTIONS: 'reflections'
}

// 用户管理
export const userService = {
  // 获取当前用户
  async getCurrentUser() {
    const { data: { user }, error } = await supabase.auth.getUser()
    return { user, error }
  },

  // 用户注册
  async signUp(email, password) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password
    })
    return { data, error }
  },

  // 用户登录
  async signIn(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    return { data, error }
  },

  // 用户登出
  async signOut() {
    const { error } = await supabase.auth.signOut()
    return { error }
  }
}

// API密钥管理
export const apiKeyService = {
  // 保存API密钥
  async saveApiKey(userId, service, key) {
    const { data, error } = await supabase
      .from(TABLES.API_KEYS)
      .upsert({
        user_id: userId,
        service: service,
        key: key,
        updated_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取用户的所有API密钥
  async getUserApiKeys(userId) {
    const { data, error } = await supabase
      .from(TABLES.API_KEYS)
      .select('*')
      .eq('user_id', userId)
    return { data, error }
  },

  // 删除API密钥
  async deleteApiKey(userId, service) {
    const { error } = await supabase
      .from(TABLES.API_KEYS)
      .delete()
      .eq('user_id', userId)
      .eq('service', service)
    return { error }
  }
}

// AI代理日志
export const agentLogService = {
  // 记录代理活动
  async logAgentActivity(userId, agent, action, details) {
    const { data, error } = await supabase
      .from(TABLES.AGENT_LOGS)
      .insert({
        user_id: userId,
        agent: agent,
        action: action,
        details: details,
        created_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取用户代理日志
  async getUserAgentLogs(userId, limit = 50) {
    const { data, error } = await supabase
      .from(TABLES.AGENT_LOGS)
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit)
    return { data, error }
  }
}

// 用户偏好设置
export const preferenceService = {
  // 保存用户偏好
  async saveUserPreferences(userId, preferences) {
    const { data, error } = await supabase
      .from(TABLES.USER_PREFERENCES)
      .upsert({
        user_id: userId,
        preferences: preferences,
        updated_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取用户偏好
  async getUserPreferences(userId) {
    const { data, error } = await supabase
      .from(TABLES.USER_PREFERENCES)
      .select('preferences')
      .eq('user_id', userId)
      .single()
    return { data, error }
  }
}

// 新闻数据
export const newsService = {
  // 保存新闻文章
  async saveNewsArticle(article) {
    const { data, error } = await supabase
      .from(TABLES.NEWS_ARTICLES)
      .insert({
        title: article.title,
        content: article.content,
        source: article.source,
        url: article.url,
        published_at: article.publishedAt,
        category: article.category,
        created_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取新闻文章
  async getNewsArticles(category = null, limit = 20) {
    let query = supabase
      .from(TABLES.NEWS_ARTICLES)
      .select('*')
      .order('published_at', { ascending: false })
      .limit(limit)
    
    if (category) {
      query = query.eq('category', category)
    }
    
    const { data, error } = await query
    return { data, error }
  }
}

// 天气数据
export const weatherService = {
  // 保存天气数据
  async saveWeatherData(location, weatherData) {
    const { data, error } = await supabase
      .from(TABLES.WEATHER_DATA)
      .insert({
        location: location,
        temperature: weatherData.temperature,
        humidity: weatherData.humidity,
        description: weatherData.description,
        icon: weatherData.icon,
        created_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取最新天气数据
  async getLatestWeatherData(location) {
    const { data, error } = await supabase
      .from(TABLES.WEATHER_DATA)
      .select('*')
      .eq('location', location)
      .order('created_at', { ascending: false })
      .limit(1)
      .single()
    return { data, error }
  }
}

// 健康记录
export const healthService = {
  // 保存健康记录
  async saveHealthRecord(userId, record) {
    const { data, error } = await supabase
      .from(TABLES.HEALTH_RECORDS)
      .insert({
        user_id: userId,
        type: record.type,
        value: record.value,
        unit: record.unit,
        notes: record.notes,
        recorded_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取用户健康记录
  async getUserHealthRecords(userId, type = null, limit = 100) {
    let query = supabase
      .from(TABLES.HEALTH_RECORDS)
      .select('*')
      .eq('user_id', userId)
      .order('recorded_at', { ascending: false })
      .limit(limit)
    
    if (type) {
      query = query.eq('type', type)
    }
    
    const { data, error } = await query
    return { data, error }
  }
}

// 任务管理
export const taskService = {
  // 创建任务
  async createTask(userId, task) {
    const { data, error } = await supabase
      .from(TABLES.TASKS)
      .insert({
        user_id: userId,
        title: task.title,
        description: task.description,
        priority: task.priority,
        due_date: task.dueDate,
        status: 'pending',
        created_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取用户任务
  async getUserTasks(userId, status = null) {
    let query = supabase
      .from(TABLES.TASKS)
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
    
    if (status) {
      query = query.eq('status', status)
    }
    
    const { data, error } = await query
    return { data, error }
  },

  // 更新任务状态
  async updateTaskStatus(taskId, status) {
    const { data, error } = await supabase
      .from(TABLES.TASKS)
      .update({ status: status, updated_at: new Date().toISOString() })
      .eq('id', taskId)
    return { data, error }
  }
}

// 反思记录
export const reflectionService = {
  // 保存反思记录
  async saveReflection(userId, reflection) {
    const { data, error } = await supabase
      .from(TABLES.REFLECTIONS)
      .insert({
        user_id: userId,
        title: reflection.title,
        content: reflection.content,
        mood: reflection.mood,
        tags: reflection.tags,
        created_at: new Date().toISOString()
      })
    return { data, error }
  },

  // 获取用户反思记录
  async getUserReflections(userId, limit = 50) {
    const { data, error } = await supabase
      .from(TABLES.REFLECTIONS)
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit)
    return { data, error }
  }
}

// 实时订阅
export const realtimeService = {
  // 订阅用户数据变化
  subscribeToUserData(userId, callback) {
    return supabase
      .channel('user_data')
      .on('postgres_changes', 
        { event: '*', schema: 'public', table: TABLES.API_KEYS, filter: `user_id=eq.${userId}` },
        callback
      )
      .subscribe()
  },

  // 订阅代理日志
  subscribeToAgentLogs(userId, callback) {
    return supabase
      .channel('agent_logs')
      .on('postgres_changes',
        { event: 'INSERT', schema: 'public', table: TABLES.AGENT_LOGS, filter: `user_id=eq.${userId}` },
        callback
      )
      .subscribe()
  }
}

// 导出Supabase客户端
export { supabase }

// 默认导出
export default {
  supabase,
  userService,
  apiKeyService,
  agentLogService,
  preferenceService,
  newsService,
  weatherService,
  healthService,
  taskService,
  reflectionService,
  realtimeService
}
