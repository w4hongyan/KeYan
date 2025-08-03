import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export const apiRequest = async <T = any>(
  endpoint: string,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET',
  data?: any,
  headers?: Record<string, string>
): Promise<ApiResponse<T>> => {
  try {
    const response = await api({
      url: endpoint,
      method,
      data,
      headers,
    });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      return {
        success: false,
        message: error.response.data?.message || error.response.data?.error || '请求失败',
        error: error.response.data?.error,
      };
    } else if (error.request) {
      return {
        success: false,
        message: '网络错误，请检查网络连接',
      };
    } else {
      return {
        success: false,
        message: '请求配置错误',
      };
    }
  }
};

export default api;