/** 开发环境走 Vite 代理；生产环境在 Vercel 配置 VITE_API_BASE_URL */
export const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api'
