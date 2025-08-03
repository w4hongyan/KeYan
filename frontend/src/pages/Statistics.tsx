import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, DatePicker, Select, Table, Tag } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, UserOutlined, FileTextOutlined, EyeOutlined, DownloadOutlined } from '@ant-design/icons';
import { Bar, Line, Pie } from '@ant-design/charts';
import { apiRequest } from '../utils/api';
import moment from 'moment';

const { RangePicker } = DatePicker;
const { Option } = Select;

interface StatisticsData {
  totalLiterature: number;
  totalViews: number;
  totalDownloads: number;
  totalUsers: number;
  weeklyUploads: Array<{
    date: string;
    count: number;
  }>;
  fieldDistribution: Array<{
    field: string;
    count: number;
  }>;
  topPapers: Array<{
    id: number;
    title: string;
    views: number;
    downloads: number;
    authors: string[];
  }>;
  userActivity: Array<{
    date: string;
    activeUsers: number;
    newUsers: number;
  }>;
}

const Statistics: React.FC = () => {
  const [statisticsData, setStatisticsData] = useState<StatisticsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [dateRange, setDateRange] = useState<[moment.Moment, moment.Moment]>([
    moment().subtract(30, 'days'),
    moment()
  ]);
  const [selectedField, setSelectedField] = useState<string>('all');

  useEffect(() => {
    fetchStatistics();
  }, [dateRange, selectedField]);

  const fetchStatistics = async () => {
    setLoading(true);
    try {
      const response = await apiRequest('/api/statistics/', 'POST', {
        start_date: dateRange[0].format('YYYY-MM-DD'),
        end_date: dateRange[1].format('YYYY-MM-DD'),
        field: selectedField
      });
      
      if (response.success) {
        setStatisticsData(response.data);
      }
    } catch (error) {
      console.error('获取统计数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const barConfig = {
    data: statisticsData?.weeklyUploads || [],
    xField: 'date',
    yField: 'count',
    height: 300,
    color: '#1890ff',
    xAxis: {
      label: {
        autoRotate: false,
      },
    },
    meta: {
      date: {
        alias: '日期',
      },
      count: {
        alias: '上传数量',
      },
    },
  };

  const pieConfig = {
    data: statisticsData?.fieldDistribution || [],
    angleField: 'count',
    colorField: 'field',
    height: 300,
    radius: 0.8,
    label: {
      type: 'outer',
      content: '{name} ({percentage})',
    },
    interactions: [
      {
        type: 'element-active',
      },
    ],
  };

  const lineConfig = {
    data: statisticsData?.userActivity || [],
    xField: 'date',
    yField: 'activeUsers',
    height: 300,
    color: '#52c41a',
    point: {
      size: 5,
      shape: 'diamond',
    },
    meta: {
      date: {
        alias: '日期',
      },
      activeUsers: {
        alias: '活跃用户',
      },
    },
  };

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      render: (text: string) => (
        <span className="truncate max-w-xs inline-block">{text}</span>
      ),
    },
    {
      title: '作者',
      dataIndex: 'authors',
      key: 'authors',
      render: (authors: string[]) => (
        <div>
          {authors.slice(0, 3).map((author, index) => (
            <Tag key={index} className="mb-1">{author}</Tag>
          ))}
          {authors.length > 3 && <Tag>...</Tag>}
        </div>
      ),
    },
    {
      title: '浏览量',
      dataIndex: 'views',
      key: 'views',
      sorter: (a: any, b: any) => a.views - b.views,
    },
    {
      title: '下载量',
      dataIndex: 'downloads',
      key: 'downloads',
      sorter: (a: any, b: any) => a.downloads - b.downloads,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">统计分析</h1>
          
          <div className="flex space-x-4 mb-4">
            <RangePicker
              value={dateRange}
              onChange={(dates) => setDateRange(dates as [moment.Moment, moment.Moment])}
              className="w-80"
            />
            <Select
              value={selectedField}
              onChange={setSelectedField}
              className="w-40"
              placeholder="选择领域"
            >
              <Option value="all">全部领域</Option>
              <Option value="machine-learning">机器学习</Option>
              <Option value="biology">生物学</Option>
              <Option value="physics">物理学</Option>
              <Option value="chemistry">化学</Option>
              <Option value="medicine">医学</Option>
            </Select>
          </div>
        </div>

        {/* 统计卡片 */}
        <Row gutter={16} className="mb-6">
          <Col span={6}>
            <Card>
              <Statistic
                title="总文献数"
                value={statisticsData?.totalLiterature || 0}
                prefix={<FileTextOutlined />}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总浏览量"
                value={statisticsData?.totalViews || 0}
                prefix={<EyeOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总下载量"
                value={statisticsData?.totalDownloads || 0}
                prefix={<DownloadOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="总用户数"
                value={statisticsData?.totalUsers || 0}
                prefix={<UserOutlined />}
                valueStyle={{ color: '#fa8c16' }}
              />
            </Card>
          </Col>
        </Row>

        {/* 图表区域 */}
        <Row gutter={16} className="mb-6">
          <Col span={12}>
            <Card title="每日文献上传趋势" loading={loading}>
              <Bar {...barConfig} />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="领域分布" loading={loading}>
              <Pie {...pieConfig} />
            </Card>
          </Col>
        </Row>

        <Row gutter={16} className="mb-6">
          <Col span={24}>
            <Card title="用户活跃度趋势" loading={loading}>
              <Line {...lineConfig} />
            </Card>
          </Col>
        </Row>

        {/* 热门论文表格 */}
        <Card title="热门论文" loading={loading}>
          <Table
            columns={columns}
            dataSource={statisticsData?.topPapers || []}
            rowKey="id"
            pagination={{
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
            }}
          />
        </Card>
      </div>
    </div>
  );
};

export default Statistics;