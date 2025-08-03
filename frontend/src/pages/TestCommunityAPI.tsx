import React, { useState, useEffect } from 'react';
import { Button, message } from 'antd';
import { communityAPI } from '../services/api';

const TestCommunityAPI: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // 检查是否有认证令牌
    const accessToken = localStorage.getItem('access_token');
    setToken(accessToken);
  }, []);

  const testGetQuestions = async () => {
    setLoading(true);
    setResult('');
    setError('');

    try {
      if (!token) {
        setError('未找到认证令牌，请先登录');
        return;
      }

      console.log('测试获取问题列表...');
      const response = await communityAPI.getQuestions({
        page: 1,
        search: '',
        tags: '',
      });

      console.log('API响应:', response);
      setResult(JSON.stringify(response, null, 2));
      message.success('获取问题列表成功');
    } catch (err) {
      console.error('获取问题列表错误:', err);
      setError(`错误: ${err.message || '未知错误'}`);
      if (err.response?.data) {
        setError(prev => prev + `\n响应数据: ${JSON.stringify(err.response.data)}`);
      }
      message.error('获取问题列表失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm max-w-4xl mx-auto mt-8">
      <h1 className="text-2xl font-bold mb-4">测试社区API</h1>

      <div className="mb-4">
        <p className="mb-2">认证状态:</p>
        {token ? (
          <p className="text-green-600">已登录 (令牌: {token.substring(0, 20)}...)</p>
        ) : (
          <p className="text-red-600">未登录</p>
        )}
      </div>

      <Button
        type="primary"
        onClick={testGetQuestions}
        loading={loading}
        disabled={!token}
      >
        测试获取问题列表
      </Button>

      {error && (
        <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md whitespace-pre-wrap">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-green-50 text-green-700 rounded-md overflow-x-auto">
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
};

export default TestCommunityAPI;