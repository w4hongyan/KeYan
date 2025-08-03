import React, { useState, useEffect } from 'react';
import { Card, Input, Button, Table, Tag, Space, Statistic, Row, Col, Select, message, Spin } from 'antd';
import { SearchOutlined, RiseOutlined, LineChartOutlined } from '@ant-design/icons';
import { apiRequest } from '../utils/api';

const { Search } = Input;
const { Option } = Select;

interface JournalInfo {
  name: string;
  abbreviation: string;
  issn: string;
  publisher: string;
  field: string;
  impact_factor_2023: number;
  rank: number;
}

interface ImpactFactorData {
  journal: string;
  year: string;
  impact_factor: number;
  total_cites: number;
  articles: number;
  cites_per_article: number;
  last_updated: string;
}

interface RankingData {
  rank: number;
  name: string;
  abbreviation: string;
  impact_factor_2023: number;
  field: string;
  quartile: string;
}

const JournalImpact: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<JournalInfo[]>([]);
  const [selectedJournal, setSelectedJournal] = useState<string>('');
  const [impactData, setImpactData] = useState<ImpactFactorData | null>(null);
  const [rankings, setRankings] = useState<RankingData[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedField, setSelectedField] = useState('all');
  const [selectedYear, setSelectedYear] = useState('2023');

  const fields = [
    { value: 'all', label: '全部领域' },
    { value: 'multidisciplinary', label: '综合' },
    { value: 'medicine', label: '医学' },
    { value: 'biology', label: '生物学' },
    { value: 'chemistry', label: '化学' },
    { value: 'physics', label: '物理学' },
    { value: 'engineering', label: '工程学' },
  ];

  const years = ['2023', '2022', '2021', '2020', '2019'];

  // 搜索期刊
  const handleSearch = async (value: string) => {
    if (!value.trim()) return;
    
    setLoading(true);
    try {
      const response = await apiRequest('/api/journals/search/', 'GET', {
        query: value
      });
      setSearchResults(response.results || []);
    } catch (error) {
      message.error('搜索期刊失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取影响因子
  const handleGetImpactFactor = async (journal: string) => {
    setLoading(true);
    try {
      const response = await apiRequest('/api/journals/get-impact-factor/', 'GET', {
        journal,
        year: selectedYear
      });
      
      if (response.error) {
        message.warning(response.suggestion || response.error);
      } else {
        setImpactData(response);
        setSelectedJournal(journal);
      }
    } catch (error) {
      message.error('获取影响因子失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取期刊排名
  const loadRankings = async () => {
    setLoading(true);
    try {
      const response = await apiRequest('/api/journals/get-journal-rankings/', 'GET', {
        field: selectedField,
        limit: 50
      });
      setRankings(response.rankings || []);
    } catch (error) {
      message.error('获取期刊排名失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRankings();
  }, [selectedField]);

  const searchColumns = [
    {
      title: '期刊名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <strong>{text}</strong>
    },
    {
      title: '缩写',
      dataIndex: 'abbreviation',
      key: 'abbreviation',
    },
    {
      title: '领域',
      dataIndex: 'field',
      key: 'field',
      render: (field: string) => <Tag color="blue">{field}</Tag>
    },
    {
      title: '2023影响因子',
      dataIndex: 'impact_factor_2023',
      key: 'impact_factor_2023',
      render: (value: number) => (
        <span style={{ color: '#1890ff', fontWeight: 'bold' }}>
          {value}
        </span>
      )
    },
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      render: (rank: number) => (
        <Tag color={rank <= 10 ? 'gold' : rank <= 50 ? 'blue' : 'default'}>
          #{rank}
        </Tag>
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record: JournalInfo) => (
        <Button 
          type="link" 
          icon={<LineChartOutlined />}
          onClick={() => handleGetImpactFactor(record.name)}
        >
          查看详情
        </Button>
      )
    }
  ];

  const rankingColumns = [
    {
      title: '排名',
      dataIndex: 'rank',
      key: 'rank',
      width: 80,
      render: (rank: number) => (
        <span style={{ 
          fontWeight: 'bold', 
          color: rank <= 10 ? '#faad14' : rank <= 50 ? '#1890ff' : '#666' 
        }}>
          #{rank}
        </span>
      )
    },
    {
      title: '期刊名称',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <strong>{text}</strong>
    },
    {
      title: '缩写',
      dataIndex: 'abbreviation',
      key: 'abbreviation',
    },
    {
      title: '2023影响因子',
      dataIndex: 'impact_factor_2023',
      key: 'impact_factor_2023',
      render: (value: number) => (
        <span style={{ color: '#1890ff', fontWeight: 'bold', fontSize: '16px' }}>
          {value}
        </span>
      )
    },
    {
      title: '领域',
      dataIndex: 'field',
      key: 'field',
      render: (field: string) => <Tag color="green">{field}</Tag>
    },
    {
      title: '分区',
      dataIndex: 'quartile',
      key: 'quartile',
      render: (quartile: string) => (
        <Tag color={quartile === 'Q1' ? 'gold' : quartile === 'Q2' ? 'blue' : 'default'}>
          {quartile}
        </Tag>
      )
    }
  ];

  return (
    <div className="journal-impact">
      <div className="page-header">
        <h1>
          <RiseOutlined /> 期刊影响因子查询
        </h1>
        <p>查询SCI期刊的最新影响因子、排名和分区信息</p>
      </div>

      <Spin spinning={loading}>
        <Row gutter={[16, 16]}>
          {/* 搜索区域 */}
          <Col span={24}>
            <Card title="期刊搜索" className="search-card">
              <Space direction="vertical" style={{ width: '100%' }}>
                <Search
                  placeholder="输入期刊名称进行搜索..."
                  allowClear
                  enterButton={<SearchOutlined />}
                  size="large"
                  onSearch={handleSearch}
                  loading={loading}
                />
                
                {impactData && (
                  <Card size="small" style={{ marginTop: 16 }}>
                    <Statistic
                      title={`${impactData.journal} ${impactData.year}年影响因子`}
                      value={impactData.impact_factor}
                      precision={3}
                      valueStyle={{ color: '#3f8600' }}
                      prefix={<RiseOutlined />}
                      suffix={
                        <span style={{ fontSize: 14, marginLeft: 8 }}>
                          总被引: {impactData.total_cites} | 
                          文章数: {impactData.articles} | 
                          篇均被引: {impactData.cites_per_article}
                        </span>
                      }
                    />
                  </Card>
                )}
              </Space>
            </Card>
          </Col>

          {/* 期刊排名 */}
          <Col span={24}>
            <Card 
              title="期刊排名" 
              extra={
                <Select
                  value={selectedField}
                  onChange={setSelectedField}
                  style={{ width: 120 }}
                >
                  {fields.map(field => (
                    <Option key={field.value} value={field.value}>
                      {field.label}
                    </Option>
                  ))}
                </Select>
              }
            >
              <Table
                columns={rankingColumns}
                dataSource={rankings}
                rowKey="rank"
                pagination={{
                  pageSize: 10,
                  showSizeChanger: true,
                  showQuickJumper: true,
                  showTotal: (total) => `共 ${total} 条记录`
                }}
              />
            </Card>
          </Col>

          {/* 搜索结果 */}
          {searchResults.length > 0 && (
            <Col span={24}>
              <Card title="搜索结果">
                <Table
                  columns={searchColumns}
                  dataSource={searchResults}
                  rowKey="name"
                  pagination={{
                    pageSize: 5,
                    showSizeChanger: true,
                    showQuickJumper: true
                  }}
                />
              </Card>
            </Col>
          )}
        </Row>
      </Spin>
    </div>
  );
};

export default JournalImpact;