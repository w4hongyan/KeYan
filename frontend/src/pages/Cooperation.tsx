import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Tag, Avatar, Space, List, Pagination, Modal, Form, Select, message, Tabs, Badge } from 'antd';
import { PlusOutlined, SearchOutlined, DollarOutlined, ClockCircleOutlined, UserOutlined, EyeOutlined } from '@ant-design/icons';
import { useSelector } from 'react-redux';
import { RootState } from '../store';
import { cooperationAPI } from '../services/api';

const { Search } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

interface CooperationPost {
  id: number;
  title: string;
  content: string;
  cooperation_type: 'mutual' | 'collab';
  publisher: string;
  publisher_avatar: string;
  budget: number | null;
  difficulty_level: string;
  status: string;
  required_skills: string[];
  tags: string[];
  view_count: number;
  application_count: number;
  created_at: string;
  deadline: string | null;
}

interface Skill {
  id: number;
  name: string;
  category: string;
}

const Cooperation: React.FC = () => {
  const [posts, setPosts] = useState<CooperationPost[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState('');
  const [selectedSkill, setSelectedSkill] = useState<string>('');
  const [selectedType, setSelectedType] = useState<string>('');
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [activeTab, setActiveTab] = useState('all');

  const user = useSelector((state: RootState) => state.auth.user);

  useEffect(() => {
    fetchPosts();
    fetchSkills();
  }, [currentPage, searchText, selectedSkill, selectedType, activeTab]);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const params: any = {
        page: currentPage,
        search: searchText,
      };
      
      if (selectedSkill) params.skills = selectedSkill;
      if (selectedType) params.cooperation_type = selectedType;
      
      if (activeTab === 'my_posts') params.my_posts = true;
      if (activeTab === 'my_applications') params.my_applications = true;
      if (activeTab === 'recommended') params.recommended = true;

      const response = await cooperationAPI.getPosts(params);
      
      // 统一处理API响应格式
      let data = response;
      if (Array.isArray(response)) {
        data = { results: response, count: response.length };
      } else if (response && typeof response === 'object') {
        if ('data' in response) {
          data = response.data;
        } else if ('results' in response) {
          data = { results: response.results, count: response.count || response.results?.length || 0 };
        } else {
          data = { results: [response], count: 1 };
        }
      } else {
        data = { results: [], count: 0 };
      }
      
      setPosts(data.results || []);
      setTotal(data.count || 0);
    } catch (error) {
      message.error('获取合作信息失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchSkills = async () => {
    try {
      const response = await cooperationAPI.getSkills();
      
      // 统一处理API响应格式
      let data = response;
      if (Array.isArray(response)) {
        data = response;
      } else if (response && typeof response === 'object') {
        if ('data' in response) {
          data = response.data;
        } else if (Array.isArray(response.results)) {
          data = response.results;
        } else {
          data = [response];
        }
      } else {
        data = [];
      }
      
      setSkills(data || []);
    } catch (error) {
      message.error('获取技能列表失败');
    }
  };

  const handleCreatePost = async (values: any) => {
    try {
      await cooperationAPI.createPost(values);
      message.success('合作信息发布成功');
      setIsModalVisible(false);
      form.resetFields();
      fetchPosts();
    } catch (error) {
      message.error('合作信息发布失败');
    }
  };

  const getDifficultyColor = (level: string) => {
    const colors: { [key: string]: string } = {
      beginner: 'green',
      intermediate: 'orange',
      advanced: 'red',
      expert: 'purple',
    };
    return colors[level] || 'default';
  };

  const getDifficultyText = (level: string) => {
    const texts: { [key: string]: string } = {
      beginner: '初级',
      intermediate: '中级',
      advanced: '高级',
      expert: '专家',
    };
    return texts[level] || level;
  };

  const getStatusColor = (status: string) => {
    const colors: { [key: string]: string } = {
      pending: 'processing',
      in_progress: 'warning',
      completed: 'success',
      cancelled: 'default',
    };
    return colors[status] || 'default';
  };

  const getStatusText = (status: string) => {
    const texts: { [key: string]: string } = {
      pending: '待接单',
      in_progress: '进行中',
      completed: '已完成',
      cancelled: '已取消',
    };
    return texts[status] || status;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow-sm rounded-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">合作交流</h1>
            <div className="flex gap-2">
              {user && (
                <Button
                  type="primary"
                  icon={<PlusOutlined />}
                  onClick={() => setIsModalVisible(true)}
                >
                  发布合作
                </Button>
              )}
            </div>
          </div>

          <Tabs
            activeKey={activeTab}
            onChange={setActiveTab}
            className="mb-6"
            items={[
              { label: '全部合作', key: 'all', children: null },
              { label: '互助', key: 'mutual', children: null },
              { label: '合作', key: 'collab', children: null },
              ...(user ? [{ label: '我的发布', key: 'my_posts', children: null }] : []),
              ...(user ? [{ label: '我的申请', key: 'my_applications', children: null }] : []),
              ...(user ? [{
                label: (
                  <Badge dot>
                    <span>推荐合作</span>
                  </Badge>
                ),
                key: 'recommended',
                children: null
              }] : [])
            ]}
          />

          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <Search
              placeholder="搜索合作信息..."
              allowClear
              enterButton={null}
              size="large"
              onSearch={(value) => {
                setSearchText(value);
                setCurrentPage(1);
              }}
              className="flex-1"
            />
            <Select
              placeholder="选择技能"
              allowClear
              style={{ width: 150 }}
              value={selectedSkill || undefined}
              onChange={(value) => {
                setSelectedSkill(value);
                setCurrentPage(1);
              }}
            >
              {skills.map(skill => (
                <Option key={skill.id} value={skill.name}>{skill.name}</Option>
              ))}
            </Select>
            <Select
              placeholder="合作类型"
              allowClear
              style={{ width: 120 }}
              value={selectedType || undefined}
              onChange={(value) => {
                setSelectedType(value);
                setCurrentPage(1);
              }}
            >
              <Option value="mutual">互助</Option>
              <Option value="collab">合作</Option>
            </Select>
          </div>
        </div>

        <List
          loading={loading}
          dataSource={posts}
          renderItem={(post) => (
            <Card key={post.id} className="mb-4 hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-start gap-4">
                <div className="flex-1">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {post.title}
                    </h3>
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                    <Avatar src={post.publisher_avatar} size={32}>
                      {post.publisher?.[0]?.toUpperCase() || 'U'}
                    </Avatar>
                    <span>{post.publisher}</span>
                    <span>·</span>
                    <span>{new Date(post.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    <Tag color={getDifficultyColor(post.difficulty_level)}>
                      {getDifficultyText(post.difficulty_level)}
                    </Tag>
                    <Tag color="blue">
                      {post.cooperation_type === 'mutual' ? '互助' : '合作'}
                    </Tag>
                    <Tag color={getStatusColor(post.status)}>
                      {getStatusText(post.status)}
                    </Tag>
                    {post.required_skills?.map(skill => (
                      <Tag key={skill} color="green">
                        {skill}
                      </Tag>
                    ))}
                    {post.tags?.map(tag => (
                      <Tag key={tag} color="purple">
                        {tag}
                      </Tag>
                    ))}
                  </div>
                  <p className="text-sm text-gray-600 line-clamp-3 mb-3">
                    {post.content}
                  </p>
                  <div className="flex flex-wrap gap-4 text-xs text-gray-500">
                    <Space>
                      <EyeOutlined />
                      <span>{post.view_count} 浏览</span>
                    </Space>
                    <Space>
                      <UserOutlined />
                      <span>{post.application_count} 申请</span>
                    </Space>
                    {post.budget && (
                      <span className="text-green-600 font-semibold">
                        预算: ¥{post.budget}
                      </span>
                    )}
                    {post.deadline && (
                      <Space>
                        <ClockCircleOutlined />
                        <span>截止: {new Date(post.deadline).toLocaleDateString()}</span>
                      </Space>
                    )}
                  </div>
                </div>
                <div className="flex flex-col gap-2 w-full md:w-40">
                  <Button
                    type="primary"
                    size="small"
                    block
                    onClick={() => {
                      // 查看详情或申请合作
                    }}
                  >
                    查看详情
                  </Button>
                  <Button
                    type="default"
                    size="small"
                    block
                    onClick={() => {
                      // 分享功能
                    }}
                  >
                    分享
                  </Button>
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
        title="发布合作信息"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
        width={800}
      >
        <Form form={form} onFinish={handleCreatePost} layout="vertical">
          <Form.Item
            name="title"
            label="标题"
            rules={[{ required: true, message: '请输入合作标题' }]}
          >
            <Input placeholder="简明扼要地描述合作需求" />
          </Form.Item>
          <Form.Item
            name="content"
            label="详细描述"
            rules={[{ required: true, message: '请输入合作详细描述' }]}
          >
            <Input.TextArea rows={4} placeholder="详细描述合作内容、背景、期望等" />
          </Form.Item>
          <div className="grid grid-cols-2 gap-4">
            <Form.Item
              name="cooperation_type"
              label="合作类型"
              rules={[{ required: true, message: '请选择合作类型' }]}
            >
              <Select placeholder="选择合作类型">
                <Option value="mutual">互助</Option>
                <Option value="collab">合作</Option>
              </Select>
            </Form.Item>
            <Form.Item
              name="difficulty_level"
              label="难度等级"
              rules={[{ required: true, message: '请选择难度等级' }]}
            >
              <Select placeholder="选择难度等级">
                <Option value="beginner">初级</Option>
                <Option value="intermediate">中级</Option>
                <Option value="advanced">高级</Option>
                <Option value="expert">专家</Option>
              </Select>
            </Form.Item>
          </div>
          <Form.Item
            name="required_skills"
            label="所需技能"
            rules={[{ required: true, message: '请选择所需技能' }]}
          >
            <Select mode="multiple" placeholder="选择所需技能">
              {skills.map(skill => (
                <Option key={skill.id} value={skill.name}>{skill.name}</Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item name="budget" label="预算（可选）">
            <Input type="number" placeholder="输入预算金额" />
          </Form.Item>
          <Form.Item name="deadline" label="截止日期（可选）">
            <Input type="date" />
          </Form.Item>
          <Form.Item name="tags" label="标签">
            <Select mode="tags" placeholder="添加标签" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              发布合作
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Cooperation;