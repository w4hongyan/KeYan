import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Divider, Typography, message } from 'antd';
import { Lock, User, ArrowRight } from 'lucide-react';
import { loginStart, loginSuccess, loginFailure } from '../store/slices/authSlice';
import { authAPI } from '../services/api';

type RootState = ReturnType<typeof import('../store').store.getState>;

const Login: React.FC = () => {
  console.log('Login component rendered');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    dispatch(loginStart());
    try {
      // 登录获取令牌
      const tokenResponse = await authAPI.login({ username, password });
      const { access, refresh } = tokenResponse;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // 获取用户信息
      const userResponse = await authAPI.getProfile();
      
      dispatch(loginSuccess({
        id: userResponse.id,
        username: userResponse.username,
        email: userResponse.email,
        token: access
      }));
      message.success('登录成功');
      navigate('/');
    } catch (err: any) {
      dispatch(loginFailure(err.response?.data?.message || err.response?.data?.detail || '登录失败'));
      message.error(err.response?.data?.message || err.response?.data?.detail || '登录失败');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-6">
          <Typography.Title level={2}>科研协作平台</Typography.Title>
          <Typography.Text>登录您的账户</Typography.Text>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User className="w-4 h-4 text-gray-400" />
              </div>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="请输入用户名"
                disabled={isLoading}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                required
              />
            </div>
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="w-4 h-4 text-gray-400" />
              </div>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="请输入密码"
                disabled={isLoading}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                required
              />
            </div>
          </div>

          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <input
                type="checkbox"
                id="remember"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
                disabled={isLoading}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="remember" className="ml-2 block text-sm text-gray-700">记住我</label>
            </div>
            <a href="#" className="text-blue-600 hover:underline text-sm" disabled={isLoading}>忘记密码?</a>
          </div>

          <div>
            <Button
              type="primary"
              htmlType="submit"
              className="w-full"
              loading={isLoading}
              disabled={isLoading}
            >
              登录
            </Button>
          </div>
        </form>

        <Divider className="my-6">
          <Typography.Text>还没有账户?</Typography.Text>
        </Divider>

        <Button
          type="default"
          className="w-full mb-3"
          onClick={() => navigate('/register')}
          disabled={isLoading}
          icon={<ArrowRight className="w-4 h-4" />}
        >
          立即注册
        </Button>

        <Divider className="my-4">
          <Typography.Text type="secondary">演示账号</Typography.Text>
        </Divider>

        <div className="space-y-2">
          <Button
            type="dashed"
            className="w-full"
            onClick={() => {
              setUsername('testuser');
              setPassword('testpass123');
            }}
            disabled={isLoading}
          >
            使用测试账号: testuser / testpass123
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default Login;