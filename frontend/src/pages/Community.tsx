import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Tag, Avatar, Space, List, Pagination, Modal, Form, Select, message } from 'antd';
import { PlusOutlined, SearchOutlined, MessageOutlined, EyeOutlined, LikeOutlined, StarOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { communityAPI } from '../services/api';

const { Search } = Input;
const { Option } = Select;

interface Question {
  id: number;
  title: string;
  content: string;
  author: string;
  author_avatar: string;
  created_at: string;
  view_count: number;
  upvote_count: number;
  collect_count: number;
  tags: Array<{ id: number; name: string; color: string }>;
  answers_count: number;
}

interface Tag {
  id: number;
  name: string;
  color: string;
}

const Community: React.FC = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState('');
  const [selectedTag, setSelectedTag] = useState<string>('');
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const user = useSelector((state: RootState) => state.auth.user);

  useEffect(() => {
    fetchQuestions();
    fetchTags();
  }, [currentPage, searchText, selectedTag]);

  const fetchQuestions = async () => {
    setLoading(true);
    try {
      console.log('请求参数:', {
        page: currentPage,
        search: searchText,
        tags: selectedTag,
      });

      const response = await communityAPI.getQuestions({
        page: currentPage,
        search: searchText,
        tags: selectedTag,
      });

      console.log('API响应:', response);

      // 检查是否是分页响应
      if (response.results) {
        setQuestions(response.results);
        setTotal(response.count);
        console.log('设置分页数据:', { results: response.results, count: response.count });
      } else {
        // 如果不是分页响应，直接使用数据
        setQuestions(response);
        setTotal(response.length);
        console.log('设置非分页数据:', { data: response, length: response.length });
      }
    } catch (error) {
      console.error('获取问题列表错误:', error);
      console.error('错误详情:', error.response?.data);

      // 处理特定错误类型
      if (error.response?.status === 401) {
        message.error('认证失败，请重新登录');
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      } else if (error.response?.status === 404) {
        message.error('请求的资源不存在');
      } else if (error.response?.status === 500) {
        message.error('服务器内部错误');
      } else {
        message.error('获取问题列表失败: ' + (error.message || '未知错误'));
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await communityAPI.getTags();
      setTags(response.data);
    } catch (error) {
      message.error('获取标签列表失败');
    }
  };

  const handleCreateQuestion = async (values: any) => {
    try {
      await communityAPI.createQuestion(values);
      message.success('问题发布成功');
      setIsModalVisible(false);
      form.resetFields();
      fetchQuestions();
    } catch (error) {
      message.error('问题发布失败');
    }
  };

  const handleSearch = (value: string) => {
    setSearchText(value);
    setCurrentPage(1);
  };

  const handleTagFilter = (tag: string) => {
    setSelectedTag(tag);
    setCurrentPage(1);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow-lg rounded-xl p-10 mb-10 border border-gray-100">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">科研社区</h1>
              <p className="text-gray-600 mt-1">分享知识，解决问题，共同进步</p>
            </div>
            <div className="flex gap-2">
              {user && (
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={() => setIsModalVisible(true)}
                  className="bg-blue-500 hover:bg-blue-600 border-0 rounded-lg"
                >
                  提问
                </Button>
              )}
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-6 mb-10">
            <Search
              placeholder="搜索问题标题或内容..."
              allowClear
              enterButton={<SearchOutlined />}
              size="large"
              onSearch={handleSearch}
              className="flex-1"
              style={{ borderRadius: '12px' }}
            />
            <Select
              placeholder="选择标签"
              allowClear
              style={{ width: 220, borderRadius: '12px' }}
              value={selectedTag || undefined}
              onChange={handleTagFilter}
              className="rounded-lg"
            >
              {(tags || []).map(tag => (
                <Option key={tag.id} value={tag.name}>
                  <Tag color={tag.color} className="rounded-full px-3 py-1">{tag.name}</Tag>
                </Option>
              ))}
            </Select>
          </div>

          <div className="flex flex-wrap gap-4 mb-10">
            {(tags || []).slice(0, 12).map(tag => (
              <Tag
                key={tag.id}
                color={tag.color}
                className="cursor-pointer hover:scale-105 transition-transform duration-200 rounded-full px-4 py-2 text-sm font-medium shadow-sm hover:shadow-md"
                onClick={() => handleTagFilter(tag.name)}
              >
                {tag.name}
              </Tag>
            ))}
          </div>
        </div>

        <List
          loading={loading}
          dataSource={questions}
          renderItem={(question) => (
            <Card key={question.id} className="mb-6 hover:shadow-xl transition-all duration-300 border-0 bg-white rounded-xl overflow-hidden">
              <div className="p-6">
                <div className="flex flex-col md:flex-row gap-6">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <Avatar 
                        src={question.author_avatar} 
                        size={40} 
                        className="ring-2 ring-gray-100 shadow-sm"
                      >
                        {question.author_name?.[0]?.toUpperCase() || 'U'}
                      </Avatar>
                      <div>
                        <span className="font-medium text-gray-900">{question.author_name}</span>
                        <span className="text-gray-500 text-sm ml-2">
                          {new Date(question.created_at).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })}
                        </span>
                      </div>
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 mb-3 hover:text-blue-600 transition-colors cursor-pointer">
                      {question.title}
                    </h3>
                    
                    <div className="flex flex-wrap gap-2 mb-4">
                      {(question.tags || []).map(tag => (
                        <Tag key={tag.id} color={tag.color} className="rounded-full px-3 py-1 text-xs font-medium">
                          {tag.name}
                        </Tag>
                      ))}
                    </div>
                    
                    <div className="flex items-center gap-6 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <EyeOutlined />
                        {question.view_count || 0} 浏览
                      </span>
                      <span className="flex items-center gap-1">
                        <MessageOutlined />
                        {question.answer_count || 0} 回答
                      </span>
                      <span className="flex items-center gap-1">
                        <LikeOutlined />
                        {question.upvote_count || 0} 点赞
                      </span>
                      <span className="flex items-center gap-1">
                        <StarOutlined />
                        {question.collect_count || 0} 收藏
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex flex-col gap-2 md:w-32">
                    <Button 
                      type="primary" 
                      icon={<EyeOutlined />}
                      className="w-full bg-blue-500 hover:bg-blue-600 border-0 rounded-lg"
                    >
                      查看详情
                    </Button>
                    <Button 
                      icon={<StarOutlined />}
                      className="w-full border-gray-300 text-gray-700 hover:border-gray-400 rounded-lg"
                    >
                      收藏
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
          )}
        />

        <div className="flex justify-center mt-6">
          <Pagination
            current={currentPage}
            total={total}
            pageSize={10}
            onChange={setCurrentPage}
            showSizeChanger={false}
          />
        </div>
      </div>

      <Modal
        title="发布问题"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        width={600}
        className="rounded-2xl"
      >
        <Form form={form} onFinish={handleCreateQuestion} layout="vertical" className="mt-8">
          <Form.Item
            name="title"
            label={<span className="font-semibold text-gray-700">问题标题</span>}
            rules={[{ required: true, message: '请输入问题标题' }]}
          >
            <Input 
              placeholder="简明扼要地描述你的问题" 
              className="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
              size="large"
            />
          </Form.Item>
          <Form.Item
            name="content"
            label={<span className="font-semibold text-gray-700">问题详情</span>}
            rules={[{ required: true, message: '请输入问题详情' }]}
          >
            <Input.TextArea 
              rows={8} 
              placeholder="详细描述你的问题背景、尝试过的解决方法、期望的结果等..."
              className="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            />
          </Form.Item>
          <Form.Item
            name="tags"
            label={<span className="font-semibold text-gray-700">选择标签</span>}
            rules={[{ required: true, message: '请至少选择一个标签' }]}
          >
            <Select 
              mode="multiple" 
              placeholder="选择相关标签"
              className="rounded-lg"
            >
              {(tags || []).map(tag => (
                <Option key={tag.id} value={tag.id}>
                  <Tag color={tag.color} className="rounded-full px-3 py-1">{tag.name}</Tag>
                </Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              block 
              size="large"
              className="bg-gradient-to-r from-blue-500 to-purple-500 border-0 hover:from-blue-600 hover:to-purple-600 rounded-lg h-14 text-xl"
            >
              发布问题
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Community;