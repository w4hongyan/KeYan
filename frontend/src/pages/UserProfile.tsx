import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { Card, Form, Input, Button, Upload, Avatar, message, Tabs, Row, Col, Space, DatePicker, Select } from 'antd';
import { UserOutlined, UploadOutlined, EditOutlined, SaveOutlined, PlusOutlined } from '@ant-design/icons';
import { useForm } from 'antd/es/form/Form';
import { apiRequest } from '../utils/api';
import { RootState } from '../store';
import moment from 'moment';

const { TabPane } = Tabs;
const { Option } = Select;

interface UserProfileData {
  id?: number;
  full_name?: string;
  bio?: string;
  education?: string;
  research_field?: string;
  institution?: string;
  position?: string;
  birth_date?: string;
  website?: string;
  orcid?: string;
}

interface BillingInfo {
  id?: number;
  full_name: string;
  company: string;
  address: string;
  phone: string;
  tax_id: string;
}

const UserProfile: React.FC = () => {
  const [form] = useForm();
  const [billingForm] = useForm();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfileData>({});
  const [billingInfos, setBillingInfos] = useState<BillingInfo[]>([]);
  const [editingBilling, setEditingBilling] = useState<number | null>(null);

  const user = useSelector((state: RootState) => state.auth.user);

  useEffect(() => {
    fetchUserProfile();
    fetchBillingInfos();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await apiRequest('/api/profile/detail/');
      if (response.success) {
        const profile = response.data;
        setUserProfile(profile);
        form.setFieldsValue({
          ...profile,
          birth_date: profile.birth_date ? moment(profile.birth_date) : null,
        });
      }
    } catch (error) {
      message.error('获取用户资料失败');
    }
  };

  const fetchBillingInfos = async () => {
    try {
      const response = await apiRequest('/api/profile/billing/');
      if (response.success) {
        setBillingInfos(response.data);
      }
    } catch (error) {
      message.error('获取账单信息失败');
    }
  };

  const handleProfileUpdate = async (values: any) => {
    setLoading(true);
    try {
      const formattedValues = {
        ...values,
        birth_date: values.birth_date ? values.birth_date.format('YYYY-MM-DD') : null,
      };
      
      const response = await apiRequest('/api/profile/detail/', 'PUT', formattedValues);
      if (response.success) {
        message.success('个人资料更新成功');
        setUserProfile(response.data);
      } else {
        message.error(response.message || '更新失败');
      }
    } catch (error) {
      message.error('更新失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAvatarUpload = async (file: File) => {
    setUploading(true);
    const formData = new FormData();
    formData.append('avatar', file);

    try {
      const response = await apiRequest('/api/profile/avatar/', 'POST', formData, {
        'Content-Type': 'multipart/form-data',
      });
      if (response.success) {
        message.success('头像上传成功');
        // 刷新用户信息
        window.location.reload();
      } else {
        message.error(response.message || '上传失败');
      }
    } catch (error) {
      message.error('上传失败');
    } finally {
      setUploading(false);
    }
  };

  const handleBillingSubmit = async (values: BillingInfo) => {
    try {
      let response;
      if (editingBilling) {
        response = await apiRequest(`/api/profile/billing/${editingBilling}/`, 'PUT', values);
      } else {
        response = await apiRequest('/api/profile/billing/', 'POST', values);
      }

      if (response.success) {
        message.success(editingBilling ? '账单信息更新成功' : '账单信息创建成功');
        fetchBillingInfos();
        billingForm.resetFields();
        setEditingBilling(null);
      } else {
        message.error(response.message || '操作失败');
      }
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleBillingEdit = (billing: BillingInfo) => {
    setEditingBilling(billing.id!);
    billingForm.setFieldsValue(billing);
    setActiveTab('billing');
  };

  const handleBillingDelete = async (id: number) => {
    try {
      const response = await apiRequest(`/api/profile/billing/${id}/`, 'DELETE');
      if (response.success) {
        message.success('删除成功');
        fetchBillingInfos();
      } else {
        message.error(response.message || '删除失败');
      }
    } catch (error) {
      message.error('删除失败');
    }
  };

  const beforeUpload = (file: File) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
      message.error('只能上传JPG/PNG格式的图片!');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('图片大小不能超过2MB!');
    }
    return isJpgOrPng && isLt2M;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">个人中心</h1>
        
        <Card className="mb-6">
          <div className="flex items-center space-x-4">
            <Upload
              name="avatar"
              showUploadList={false}
              beforeUpload={beforeUpload}
              customRequest={({ file }) => handleAvatarUpload(file as File)}
            >
              <Avatar
                size={100}
                src={user?.avatar}
                icon={<UserOutlined />}
                className="cursor-pointer"
              />
            </Upload>
            <div>
              <h2 className="text-xl font-semibold">{user?.nickname || user?.username}</h2>
              <p className="text-gray-600">{user?.email}</p>
              <p className="text-gray-500">积分: {user?.points}</p>
            </div>
          </div>
        </Card>

        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="个人资料" key="profile">
            <Card>
              <Form
                form={form}
                layout="vertical"
                onFinish={handleProfileUpdate}
                initialValues={userProfile}
              >
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      label="姓名"
                      name="full_name"
                      rules={[{ required: true, message: '请输入姓名' }]}
                    >
                      <Input placeholder="请输入姓名" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item label="出生日期" name="birth_date">
                      <DatePicker className="w-full" placeholder="选择出生日期" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item label="个人简介" name="bio">
                  <Input.TextArea rows={4} placeholder="简单介绍一下自己..." />
                </Form.Item>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item label="教育背景" name="education">
                      <Select placeholder="选择最高学历">
                        <Option value="高中">高中</Option>
                        <Option value="本科">本科</Option>
                        <Option value="硕士">硕士</Option>
                        <Option value="博士">博士</Option>
                        <Option value="博士后">博士后</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item label="研究领域" name="research_field">
                      <Input placeholder="例如：机器学习、生物信息学" />
                    </Form.Item>
                  </Col>
                </Row>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item label="机构/学校" name="institution">
                      <Input placeholder="所在机构或学校" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item label="职位" name="position">
                      <Input placeholder="例如：研究员、教授、学生" />
                    </Form.Item>
                  </Col>
                </Row>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item label="个人网站" name="website">
                      <Input placeholder="https://example.com" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item label="ORCID" name="orcid">
                      <Input placeholder="0000-0000-0000-0000" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item>
                  <Button type="primary" htmlType="submit" loading={loading} icon={<SaveOutlined />}>
                    保存修改
                  </Button>
                </Form.Item>
              </Form>
            </Card>
          </TabPane>

          <TabPane tab="账单信息" key="billing">
            <Card>
              <Form
                form={billingForm}
                layout="vertical"
                onFinish={handleBillingSubmit}
              >
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      label="姓名"
                      name="full_name"
                      rules={[{ required: true, message: '请输入姓名' }]}
                    >
                      <Input placeholder="请输入姓名" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      label="公司/机构"
                      name="company"
                      rules={[{ required: true, message: '请输入公司或机构名称' }]}
                    >
                      <Input placeholder="请输入公司或机构名称" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item
                  label="地址"
                  name="address"
                  rules={[{ required: true, message: '请输入详细地址' }]}
                >
                  <Input.TextArea rows={3} placeholder="请输入详细地址" />
                </Form.Item>

                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item
                      label="联系电话"
                      name="phone"
                      rules={[{ required: true, message: '请输入联系电话' }]}
                    >
                      <Input placeholder="请输入联系电话" />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item
                      label="税号"
                      name="tax_id"
                      rules={[{ required: true, message: '请输入税号' }]}
                    >
                      <Input placeholder="请输入税号" />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item>
                  <Space>
                    <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
                      {editingBilling ? '更新' : '创建'}
                    </Button>
                    {editingBilling && (
                      <Button onClick={() => {
                        setEditingBilling(null);
                        billingForm.resetFields();
                      }}>
                        取消
                      </Button>
                    )}
                  </Space>
                </Form.Item>
              </Form>

              {billingInfos.length > 0 && (
                <div className="mt-6">
                  <h3 className="text-lg font-semibold mb-4">已有账单信息</h3>
                  {billingInfos.map((billing) => (
                    <Card key={billing.id} className="mb-4" size="small">
                      <div className="flex justify-between items-start">
                        <div>
                          <p><strong>姓名:</strong> {billing.full_name}</p>
                          <p><strong>公司:</strong> {billing.company}</p>
                          <p><strong>地址:</strong> {billing.address}</p>
                          <p><strong>电话:</strong> {billing.phone}</p>
                          <p><strong>税号:</strong> {billing.tax_id}</p>
                        </div>
                        <Space>
                          <Button
                            type="link"
                            icon={<EditOutlined />}
                            onClick={() => handleBillingEdit(billing)}
                          >
                            编辑
                          </Button>
                          <Button
                            type="link"
                            danger
                            onClick={() => handleBillingDelete(billing.id!)}
                          >
                            删除
                          </Button>
                        </Space>
                      </div>
                    </Card>
                  ))}
                </div>
              )}
            </Card>
          </TabPane>
        </Tabs>
      </div>
    </div>
  );
};

export default UserProfile;