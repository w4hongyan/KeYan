import React from 'react';
import { Button, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import { Home as HomeIcon } from 'lucide-react';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gray-50 p-4 text-center">
      <Typography.Title level={1} className="text-9xl font-bold text-gray-200 mb-6">404</Typography.Title>
      <Typography.Title level={2} className="text-2xl font-semibold text-gray-800 mb-4">页面不存在</Typography.Title>
      <Typography.Text className="text-gray-600 mb-8 max-w-md">
        很抱歉，您访问的页面不存在。可能是链接有误或页面已被移除。
      </Typography.Text>
      <Button
        type="primary"
        size="large"
        onClick={() => navigate('/')}
        icon={<HomeIcon className="w-5 h-5 mr-2" />}
      >
        返回首页
      </Button>
    </div>
  );
};

export default NotFound;