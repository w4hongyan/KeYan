import React, { useState } from 'react';
import { Card, Row, Col, Button, Upload, Input, Tabs, Space, Progress, Alert, Typography, List, Tag } from 'antd';
import { UploadOutlined, SearchOutlined, FileTextOutlined, LinkOutlined } from '@ant-design/icons';
import { apiRequest } from '../utils/api';

const { TextArea } = Input;
const { Title, Text } = Typography;

interface SimilarityResult {
  similarity_score: number;
  similarity_percentage: number;
  risk_level: string;
  analysis?: {
    sentence_matches?: Array<{
      original: string;
      matched: string;
      similarity: number;
    }>;
    common_keywords?: string[];
    keyword_similarity?: number;
    sentence_coverage?: number;
  };
  recommendations?: string[];
}

interface LiteratureResult {
  literature_id: number;
  title: string;
  authors: string[];
  similarity: number;
  similarity_percentage: number;
  risk_level: string;
}

interface CheckResults {
  total_checked?: number;
  high_risk?: number;
  medium_risk?: number;
  low_risk?: number;
  results?: LiteratureResult[];
}

const PlagiarismCheck: React.FC = () => {
  const [text1, setText1] = useState<string>('');
  const [text2, setText2] = useState<string>('');
  const [literatureId, setLiteratureId] = useState<string>('');
  const [url, setUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [results, setResults] = useState<SimilarityResult | CheckResults | null>(null);
  const [activeTab, setActiveTab] = useState<string>('text');

  const handleTextCheck = async () => {
    if (!text1 || !text2) {
      return;
    }

    setLoading(true);
    try {
      const response = await apiRequest('/api/plagiarism/check_similarity/', 'POST', {
        text1,
        text2,
      });
      
      if (response.success) {
        setResults(response.data);
      }
    } catch (error) {
      console.error('查重检查失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLiteratureCheck = async () => {
    if (!literatureId && !text1) {
      return;
    }

    setLoading(true);
    try {
      const response = await apiRequest('/api/plagiarism/check_literature/', 'POST', {
        literature_id: literatureId || undefined,
        text: text1 || undefined,
      });
      
      if (response.success) {
        setResults(response.data);
      }
    } catch (error) {
      console.error('文献查重检查失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUrlCheck = async () => {
    if (!url || !text1) {
      return;
    }

    setLoading(true);
    try {
      const response = await apiRequest('/api/plagiarism/check_url/', 'POST', {
        url,
        text: text1,
      });
      
      if (response.success) {
        setResults(response.data);
      }
    } catch (error) {
      console.error('URL查重检查失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'high':
        return '#ff4d4f';
      case 'medium':
        return '#faad14';
      case 'low':
        return '#52c41a';
      default:
        return '#1890ff';
    }
  };

  const getRiskText = (level: string) => {
    switch (level) {
      case 'high':
        return '高风险';
      case 'medium':
        return '中等风险';
      case 'low':
        return '低风险';
      default:
        return '未知';
    }
  };

  const renderTextResults = (result: SimilarityResult) => (
    <Space direction="vertical" className="w-full">
      <Card>
        <Title level={4}>相似度分析结果</Title>
        <Progress
          type="circle"
          percent={result.similarity_percentage}
          strokeColor={getRiskColor(result.risk_level)}
          format={(percent) => `${percent}%`}
          size={120}
        />
        <div className="mt-4">
          <Tag color={getRiskColor(result.risk_level)}>
            {getRiskText(result.risk_level)}
          </Tag>
        </div>
      </Card>

      {result.analysis && (
        <>
          {result.analysis.sentence_matches && result.analysis.sentence_matches.length > 0 && (
            <Card title="相似句子">
              <List
                dataSource={result.analysis.sentence_matches.slice(0, 5)}
                renderItem={(item) => (
                  <List.Item>
                    <div>
                      <Text strong>原文:</Text> {item.original}
                      <br />
                      <Text strong>匹配:</Text> {item.matched}
                      <br />
                      <Text type="secondary">相似度: {item.similarity * 100}%</Text>
                    </div>
                  </List.Item>
                )}
              />
            </Card>
          )}

          {result.analysis.common_keywords && result.analysis.common_keywords.length > 0 && (
            <Card title="共同关键词">
              <Space wrap>
                {result.analysis.common_keywords.map((keyword, index) => (
                  <Tag key={index} color="blue">{keyword}</Tag>
                ))}
              </Space>
            </Card>
          )}
        </>
      )}

      {result.recommendations && (
        <Card title="建议">
          <List
            dataSource={result.recommendations}
            renderItem={(item) => (
              <List.Item>
                <Alert message={item} type="info" showIcon />
              </List.Item>
            )}
          />
        </Card>
      )}
    </Space>
  );

  const renderLiteratureResults = (result: CheckResults) => (
    <Space direction="vertical" className="w-full">
      <Card>
        <Title level={4}>文献查重结果</Title>
        <Row gutter={16}>
          <Col span={8}>
            <Card>
              <Title level={5}>总计检查</Title>
              <Text style={{ fontSize: 24 }}>{result.total_checked}</Text>
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Title level={5}>高风险</Title>
              <Text style={{ fontSize: 24, color: '#ff4d4f' }}>{result.high_risk}</Text>
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Title level={5}>中等风险</Title>
              <Text style={{ fontSize: 24, color: '#faad14' }}>{result.medium_risk}</Text>
            </Card>
          </Col>
        </Row>
      </Card>

      <Card title="详细结果">
        <List
          dataSource={result.results}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                title={item.title}
                description={
                  <Space>
                    <Text>作者: {item.authors.join(', ')}</Text>
                    <Tag color={getRiskColor(item.risk_level)}>
                      {getRiskText(item.risk_level)} ({item.similarity_percentage}%)
                    </Tag>
                  </Space>
                }
              />
            </List.Item>
          )}
        />
      </Card>
    </Space>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <Title level={2}>论文查重服务</Title>
        <Text type="secondary">
          使用先进的文本相似度检测算法，帮助您识别潜在的抄袭内容
        </Text>

        <Tabs activeKey={activeTab} onChange={setActiveTab} className="mt-6">
          <Tabs.TabPane tab="文本对比" key="text">
            <Row gutter={16}>
              <Col span={12}>
                <Card title="原文本">
                  <TextArea
                    rows={8}
                    placeholder="请输入第一段文本..."
                    value={text1}
                    onChange={(e) => setText1(e.target.value)}
                  />
                </Card>
              </Col>
              <Col span={12}>
                <Card title="对比文本">
                  <TextArea
                    rows={8}
                    placeholder="请输入第二段文本..."
                    value={text2}
                    onChange={(e) => setText2(e.target.value)}
                  />
                </Card>
              </Col>
            </Row>
            <div className="mt-4">
              <Button
                type="primary"
                icon={<SearchOutlined />}
                onClick={handleTextCheck}
                loading={loading}
                disabled={!text1 || !text2}
              >
                开始查重
              </Button>
            </div>
          </Tabs.TabPane>

          <Tabs.TabPane tab="文献查重" key="literature">
            <Row gutter={16}>
              <Col span={12}>
                <Card title="待检查文本">
                  <TextArea
                    rows={8}
                    placeholder="请输入要检查的文本..."
                    value={text1}
                    onChange={(e) => setText1(e.target.value)}
                  />
                </Card>
              </Col>
              <Col span={12}>
                <Card title="检查选项">
                  <Space direction="vertical" className="w-full">
                    <Input
                      placeholder="文献ID（可选）"
                      value={literatureId}
                      onChange={(e) => setLiteratureId(e.target.value)}
                    />
                    <Text type="secondary">
                      留空则直接检查输入的文本
                    </Text>
                  </Space>
                </Card>
              </Col>
            </Row>
            <div className="mt-4">
              <Button
                type="primary"
                icon={<FileTextOutlined />}
                onClick={handleLiteratureCheck}
                loading={loading}
                disabled={!text1 && !literatureId}
              >
                检查文献
              </Button>
            </div>
          </Tabs.TabPane>

          <Tabs.TabPane tab="网页查重" key="url">
            <Row gutter={16}>
              <Col span={12}>
                <Card title="待检查文本">
                  <TextArea
                    rows={8}
                    placeholder="请输入要检查的文本..."
                    value={text1}
                    onChange={(e) => setText1(e.target.value)}
                  />
                </Card>
              </Col>
              <Col span={12}>
                <Card title="网页地址">
                  <Input
                    placeholder="请输入网页URL"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    prefix={<LinkOutlined />}
                  />
                </Card>
              </Col>
            </Row>
            <div className="mt-4">
              <Button
                type="primary"
                icon={<LinkOutlined />}
                onClick={handleUrlCheck}
                loading={loading}
                disabled={!text1 || !url}
              >
                检查网页
              </Button>
            </div>
          </Tabs.TabPane>
        </Tabs>

        {results && (
          <div className="mt-6">
            {activeTab === 'text' && 'similarity_score' in results && renderTextResults(results as SimilarityResult)}
            {activeTab === 'literature' && 'total_checked' in results && renderLiteratureResults(results as CheckResults)}
            {activeTab === 'url' && 'similarity_score' in results && renderTextResults(results as SimilarityResult)}
          </div>
        )}
      </div>
    </div>
  );
};

export default PlagiarismCheck;