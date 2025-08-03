import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { Card, Button, Divider, Typography, message } from 'antd';import { User, Mail, Lock, ArrowLeft } from 'lucide-react';
import { authAPI } from '../services/api';

type RootState = ReturnType<typeof import('../store').store.getState>;

const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [nickname, setNickname] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isLoading } = useSelector((state: RootState) => state.auth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 表单验证
    if (!username) {
      message.error('请输入用户名');
      return;
    }

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      message.error('请输入有效的邮箱地址');
      return;
    }

    if (!password || password.length < 6) {
      message.error('密码长度至少为6位');
      return;
    }

    if (password !== confirmPassword) {
      message.error('两次输入的密码不一致');
      return;
    }

    try {
      await authAPI.register({ username, email, password, nickname });
      message.success('注册成功！请登录。');
      navigate('/login');
    } catch (err: any) {
      let errorMessage = '注册失败';
      
      if (err.response?.data) {
        const data = err.response.data;
        
        // 处理自定义ApiResponse错误格式
        if (data.errors) {
          // 收集所有字段的错误信息
          const fieldErrors = Object.values(data.errors).flat();
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors[0] as string;
          } else {
            errorMessage = data.message || '注册失败';
          }
        } else if (typeof data === 'object' && !data.detail) {
          // 处理DRF验证错误格式
          const fieldErrors = Object.values(data).flat();
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors[0] as string;
          }
        } else {
          // 处理统一格式或其他格式
          errorMessage = data.detail || data.message || '注册失败';
        }
      }
      
      message.error(errorMessage);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 p-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-6">
          <Typography.Title level={2}>科研协作平台</Typography.Title>
          <Typography.Text>创建新账户</Typography.Text>
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
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Mail className="w-4 h-4 text-gray-400" />
              </div>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="请输入邮箱"
                disabled={isLoading}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>

          <div>
            <label htmlFor="nickname" className="block text-sm font-medium text-gray-700 mb-1">昵称</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User className="w-4 h-4 text-gray-400" />
              </div>
              <input
                type="text"
                id="nickname"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                placeholder="请输入昵称"
                disabled={isLoading}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
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
              />
            </div>
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Lock className="w-4 h-4 text-gray-400" />
              </div>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="请确认密码"
                disabled={isLoading}
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>

          <div>
            <Button
              type="primary"
              htmlType="submit"
              className="w-full"
              loading={isLoading}
              disabled={isLoading}
            >
              注册
            </Button>
          </div>
        </form>

        <Divider className="my-6">
          <Typography.Text>已有账户?</Typography.Text>
        </Divider>

        <Button
          type="default"
          className="w-full"
          onClick={() => navigate('/login')}
          disabled={isLoading}
          icon={<ArrowLeft className="w-4 h-4" />}
        >
          返回登录
        </Button>
      </Card>
    </div>
  );
};

export default Register;