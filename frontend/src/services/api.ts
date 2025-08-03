import axios from 'axios';
import { store } from '../store';
import { logout } from '../store/slices/authSlice';

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

// 统一响应格式处理函数
const handleResponse = (response: any) => {
  // 检查是否为统一格式响应
  if (response.data && typeof response.data === 'object' && 'success' in response.data) {
    if (response.data.success) {
      // 成功响应
      return response.data.data;
    } else {
      // 错误响应
      const error = new Error(response.data.message || '请求失败');
      // 将完整错误数据附加到error对象
      error.response = { data: response.data };
      throw error;
    }
  } else {
    // 处理非统一格式响应
    return response.data;
  }
};

// 统一错误处理函数
const handleError = (error: any) => {
  console.log('===== 错误处理开始 =====');
  console.log('错误响应详情:', error);
  let message = '未知错误';
  
  // 保留原始错误的响应数据
  const originalResponse = error.response;
  
  if (originalResponse) {
    // 服务器返回了错误响应
    const status = originalResponse.status;
    console.log('错误状态码:', status);
    console.log('错误数据:', originalResponse.data);
    
    // 检查是否为401未授权错误，更新Redux状态
    if (status === 401) {
      // 清除本地存储的用户信息
      localStorage.removeItem('access_token');
      // 更新Redux状态，触发路由守卫跳转
      store.dispatch(logout());
    }
    
    // 检查是否为统一格式错误
    if (originalResponse.data && typeof originalResponse.data === 'object' && 'success' in originalResponse.data) {
      // 统一格式错误
      message = originalResponse.data.message || `请求失败 (${status})`;
    } else {
      // 非统一格式错误
      message = originalResponse.data.message || originalResponse.data.detail || `请求失败 (${status})`;
    }
  } else if (error.request) {
    // 请求已发送但未收到响应
    message = '未收到服务器响应';
    console.log('未收到服务器响应:', error.request);
  } else {
    // 设置请求时发生错误
    message = `请求错误: ${error.message}`;
    console.log('请求错误:', error.message);
  }
  
  console.log('最终错误消息:', message);
  console.log('===== 错误处理结束 =====');
  
  // 创建新的错误对象，保留原始错误的响应数据
  const newError = new Error(message);
  newError.response = originalResponse;
  
  throw newError;
}


// 响应拦截器
api.interceptors.response.use(handleResponse, handleError);

export default api;

// API服务
export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post('/api/login/', credentials),
  
  register: (userData: { username: string; email: string; password: string }) => {
    // 创建一个不使用全局拦截器的axios实例
    const noAuthApi = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    // 添加响应处理但不添加请求拦截器
    noAuthApi.interceptors.response.use(handleResponse, handleError);
    return noAuthApi.post('/api/register/', userData);
  },
  
  refresh: (refresh: string) =>
    api.post('/api/token/refresh/', { refresh }),
  
  getProfile: () =>
    api.get('/api/profile/'),
};

export const literatureAPI = {
  getLiterature: (params?: any) =>
    api.get('/api/literature/literatures/', { params }),
  
  getLiteratureDetail: (id: number) =>
    api.get(`/api/literature/literatures/${id}/`),
  
  createLiterature: (data: any) =>
    api.post('/api/literature/literatures/', data),
  
  updateLiterature: (id: number, data: any) =>
    api.put(`/api/literature/literatures/${id}/`, data),
  
  deleteLiterature: (id: number) =>
    api.delete(`/api/literature/literatures/${id}/`),
  
  getJournals: (params?: any) =>
    api.get('/api/literature/journals/', { params }),
  
  searchPubMed: (query: string) =>
    api.get('/api/literature/search-pubmed/', { params: { q: query } }),
  
  importFromPubMed: (pmid: string) =>
    api.post('/api/literature/import-pubmed/', { pmid }),
  
  translateLiterature: (id: number, targetLang: string = 'zh') =>
    api.post(`/api/literature/literatures/${id}/translate/`, { target_lang: targetLang }),
};

export const communityAPI = {
  getQuestions: (params?: any) =>
    api.get('/api/community/questions/', { params }),
  
  getQuestionDetail: (id: number) =>
    api.get(`/api/community/questions/${id}/`),
  
  createQuestion: (data: any) =>
    api.post('/api/community/questions/', data),
  
  updateQuestion: (id: number, data: any) =>
    api.put(`/api/community/questions/${id}/`, data),
  
  deleteQuestion: (id: number) =>
    api.delete(`/api/community/questions/${id}/`),
  
  createAnswer: (questionId: number, data: any) =>
    api.post(`/api/community/questions/${questionId}/answers/`, data),
  
  updateAnswer: (answerId: number, data: any) =>
    api.put(`/api/community/answers/${answerId}/`, data),
  
  deleteAnswer: (answerId: number) =>
    api.delete(`/api/community/answers/${answerId}/`),
  
  upvoteQuestion: (id: number) =>
    api.post(`/api/community/questions/${id}/upvote/`),
  
  upvoteAnswer: (id: number) =>
    api.post(`/api/community/answers/${id}/upvote/`),
  
  collectQuestion: (id: number) =>
    api.post(`/api/community/questions/${id}/collect/`),
  
  getTags: () =>
    api.get('/api/community/tags/'),
  
  getMyCollections: () =>
    api.get('/api/community/collections/'),
};

export const cooperationAPI = {
  getPosts: (params?: any) =>
    api.get('/api/cooperation/posts/', { params }),
  
  getPostDetail: (id: number) =>
    api.get(`/api/cooperation/posts/${id}/`),
  
  createPost: (data: any) =>
    api.post('/api/cooperation/posts/', data),
  
  updatePost: (id: number, data: any) =>
    api.put(`/api/cooperation/posts/${id}/`, data),
  
  deletePost: (id: number) =>
    api.delete(`/api/cooperation/posts/${id}/`),
  
  applyForCooperation: (postId: number, data: any) =>
    api.post(`/api/cooperation/posts/${postId}/apply/`, data),
  
  getMyApplications: () =>
    api.get('/api/cooperation/applications/'),
  
  updateApplicationStatus: (applicationId: number, status: string) =>
    api.put(`/api/cooperation/applications/${applicationId}/`, { status }),
  
  getSkills: () =>
    api.get('/api/cooperation/skills/'),
  
  createUserSkill: (data: any) =>
    api.post('/api/cooperation/user-skills/', data),
  
  updateUserSkill: (skillId: number, data: any) =>
    api.put(`/api/cooperation/user-skills/${skillId}/`, data),
  
  deleteUserSkill: (skillId: number) =>
    api.delete(`/api/cooperation/user-skills/${skillId}/`),
  
  getProgress: (postId: number) =>
    api.get(`/api/cooperation/posts/${postId}/progress/`),
  
  updateProgress: (postId: number, data: any) =>
    api.post(`/api/cooperation/posts/${postId}/progress/`, data),
};