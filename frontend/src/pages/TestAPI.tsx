import React, { useState } from 'react';
import { authAPI, literatureAPI } from '../services/api';
import ErrorDisplay from '../components/ErrorDisplay';

const TestAPI: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [errorDetails, setErrorDetails] = useState<any>(null);

  const testSuccess = async () => {
    try {
      setError('');
      setErrorDetails(null);
      // 测试成功的API调用
      const data = await literatureAPI.getTags();
      setResult(`成功获取标签: ${JSON.stringify(data)}`);
    } catch (err: any) {
      setError(`错误: ${err.message}`);
      setErrorDetails(err);
    }
  };

  const testNotFound = async () => {
    try {
      setError('');
      setErrorDetails(null);
      // 测试不存在的API接口
      await literatureAPI.getLiteratureDetail(9999);
    } catch (err: any) {
      setError(`错误: ${err.message}`);
      setErrorDetails(err);
    }
  };

  const testUnauthorized = async () => {
    try {
      setError('');
      setErrorDetails(null);
      // 保存当前token
      const oldToken = localStorage.getItem('access_token');
      // 移除token以模拟未授权状态
      localStorage.removeItem('access_token');
      // 调用需要认证的API
      await authAPI.getProfile();
    } catch (err: any) {
      setError(`错误: ${err.message}`);
      setErrorDetails(err);
    }
  };

  const testRegister = async () => {
    try {
      setError('');
      setErrorDetails(null);
      setResult('');
      // 测试注册功能（使用已存在的用户名和邮箱）
      await authAPI.register({
        username: 'testuser',
        email: 'admin@example.com', // 已存在的邮箱
        password: 'testpassword123'
      });
      setResult('注册成功');
    } catch (err: any) {
      console.log('注册错误详情:', err);
      // 处理统一格式的错误响应
      if (err.response && err.response.data) {
        const errorData = err.response.data;
        setError(`错误: ${errorData.message || err.message || '注册失败'}`);
        setErrorDetails(err);
      } else {
        setError(`错误: ${err.message || '注册失败'}`);
        setErrorDetails(err);
      }
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto bg-white shadow-md rounded-lg mt-8">
      <h1 className="text-xl font-bold mb-4">API响应测试</h1>
      <div className="space-y-4">
        <button
          onClick={testSuccess}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          测试成功响应
        </button>
        <button
          onClick={testNotFound}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          测试404错误
        </button>
        <button
          onClick={testUnauthorized}
          className="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600"
        >
          测试401未授权
        </button>
        <button
          onClick={testRegister}
          className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
        >
          测试注册错误
        </button>
      </div>

      {result && (
        <div className="mt-4 p-3 bg-green-100 rounded">
          <h3 className="font-bold text-green-700">成功结果:</h3>
          <p>{result}</p>
        </div>
      )}

      {error && (
        <>
          <div className="mt-4 p-3 bg-red-100 rounded">
            <h3 className="font-bold text-red-700">错误信息:</h3>
            <p>{error}</p>
          </div>
          <ErrorDisplay error={errorDetails} />
        </>
      )}
    </div>
  );
};

export default TestAPI;