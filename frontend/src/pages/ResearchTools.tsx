import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, Select, Upload, message, Tabs, Space, Form, Input, Slider } from 'antd';
import { UploadOutlined, DownloadOutlined, BarChartOutlined, LineChartOutlined, PieChartOutlined, AreaChartOutlined } from '@ant-design/icons';
import { Bar, Line, Pie, Area, Column, Scatter } from '@ant-design/charts';
import { apiRequest } from '../utils/api';

const { Option } = Select;
const { TabPane } = Tabs;
const { TextArea } = Input;

interface ChartData {
  x: string;
  y: number;
  category?: string;
}

interface ResearchData {
  id: number;
  title: string;
  data: any[];
  chart_type: string;
  created_at: string;
}

const ResearchTools: React.FC = () => {
  const [chartType, setChartType] = useState<string>('bar');
  const [dataSource, setDataSource] = useState<ChartData[]>([]);
  const [customData, setCustomData] = useState<string>('');
  const [savedCharts, setSavedCharts] = useState<ResearchData[]>([]);
  const [chartTitle, setChartTitle] = useState<string>('');
  const [xLabel, setXLabel] = useState<string>('X轴');
  const [yLabel, setYLabel] = useState<string>('Y轴');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSavedCharts();
    loadSampleData();
  }, []);

  const fetchSavedCharts = async () => {
    try {
      const response = await apiRequest('/api/research/charts/');
      if (response.success) {
        setSavedCharts(response.data);
      }
    } catch (error) {
      console.error('获取保存的图表失败:', error);
    }
  };

  const loadSampleData = () => {
    const sampleData = [
      { x: 'Jan', y: 100 },
      { x: 'Feb', y: 120 },
      { x: 'Mar', y: 80 },
      { x: 'Apr', y: 140 },
      { x: 'May', y: 110 },
      { x: 'Jun', y: 160 },
    ];
    setDataSource(sampleData);
  };

  const handleDataUpload = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target?.result as string);
        setDataSource(data);
        message.success('数据上传成功');
      } catch (error) {
        message.error('数据格式错误，请上传JSON格式文件');
      }
    };
    reader.readAsText(file);
    return false;
  };

  const handleCustomDataSubmit = () => {
    try {
      const data = JSON.parse(customData);
      setDataSource(data);
      message.success('数据更新成功');
    } catch (error) {
      message.error('JSON格式错误');
    }
  };

  const generateChartConfig = () => {
    const baseConfig = {
      data: dataSource,
      xField: 'x',
      yField: 'y',
      height: 400,
      xAxis: { title: { text: xLabel } },
      yAxis: { title: { text: yLabel } },
      color: '#1890ff',
    };

    switch (chartType) {
      case 'bar':
        return { ...baseConfig, type: 'column' };
      case 'line':
        return { ...baseConfig, type: 'line', point: { size: 5, shape: 'diamond' } };
      case 'area':
        return { ...baseConfig, type: 'area' };
      case 'pie':
        return {
          type: 'pie',
          data: dataSource,
          angleField: 'y',
          colorField: 'x',
          radius: 0.8,
          label: { type: 'outer', content: '{name} ({percentage})' },
          height: 400,
        };
      case 'scatter':
        return { ...baseConfig, type: 'scatter' };
      default:
        return baseConfig;
    }
  };

  const saveChart = async () => {
    if (!chartTitle) {
      message.error('请输入图表标题');
      return;
    }

    try {
      const response = await apiRequest('/api/research/charts/', 'POST', {
        title: chartTitle,
        data: dataSource,
        chart_type: chartType,
        config: {
          x_label: xLabel,
          y_label: yLabel,
        },
      });

      if (response.success) {
        message.success('图表保存成功');
        fetchSavedCharts();
      }
    } catch (error) {
      message.error('保存失败');
    }
  };

  const loadChart = (chart: ResearchData) => {
    setDataSource(chart.data);
    setChartType(chart.chart_type);
    setChartTitle(chart.title);
    setSavedCharts([]);
  };

  const deleteChart = async (id: number) => {
    try {
      const response = await apiRequest(`/api/research/charts/${id}/`, 'DELETE');
      if (response.success) {
        message.success('删除成功');
        fetchSavedCharts();
      }
    } catch (error) {
      message.error('删除失败');
    }
  };

  const downloadChart = () => {
    const canvas = document.querySelector('canvas');
    if (canvas) {
      const url = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = `${chartTitle || 'chart'}.png`;
      link.href = url;
      link.click();
    }
  };

  const ChartComponent = () => {
    const config = generateChartConfig();
    switch (chartType) {
      case 'bar':
        return <Column {...config} />;
      case 'line':
        return <Line {...config} />;
      case 'area':
        return <Area {...config} />;
      case 'pie':
        return <Pie {...config} />;
      case 'scatter':
        return <Scatter {...config} />;
      default:
        return <Bar {...config} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">科研绘图工具</h1>

        <Tabs defaultActiveKey="create">
          <TabPane tab="创建图表" key="create">
            <Row gutter={16}>
              <Col span={8}>
                <Card title="数据设置" className="mb-4">
                  <Space direction="vertical" className="w-full">
                    <Input
                      placeholder="图表标题"
                      value={chartTitle}
                      onChange={(e) => setChartTitle(e.target.value)}
                    />
                    <Select
                      value={chartType}
                      onChange={setChartType}
                      className="w-full"
                    >
                      <Option value="bar">柱状图</Option>
                      <Option value="line">折线图</Option>
                      <Option value="area">面积图</Option>
                      <Option value="pie">饼图</Option>
                      <Option value="scatter">散点图</Option>
                    </Select>
                    <Input
                      placeholder="X轴标签"
                      value={xLabel}
                      onChange={(e) => setXLabel(e.target.value)}
                    />
                    <Input
                      placeholder="Y轴标签"
                      value={yLabel}
                      onChange={(e) => setYLabel(e.target.value)}
                    />
                  </Space>
                </Card>

                <Card title="数据输入">
                  <Tabs>
                    <TabPane tab="上传文件" key="upload">
                      <Upload
                        accept=".json"
                        beforeUpload={handleDataUpload}
                        maxCount={1}
                      >
                        <Button icon={<UploadOutlined />}>上传JSON文件</Button>
                      </Upload>
                    </TabPane>
                    <TabPane tab="手动输入" key="manual">
                      <TextArea
                        rows={8}
                        placeholder='输入JSON格式数据，例如：[{"x":"A","y":10},{"x":"B","y":20}]'
                        value={customData}
                        onChange={(e) => setCustomData(e.target.value)}
                      />
                      <Button onClick={handleCustomDataSubmit} className="mt-2">
                        应用数据
                      </Button>
                    </TabPane>
                  </Tabs>
                </Card>

                <Card>
                  <Space>
                    <Button type="primary" onClick={saveChart} loading={loading}>
                      保存图表
                    </Button>
                    <Button icon={<DownloadOutlined />} onClick={downloadChart}>
                      下载图片
                    </Button>
                  </Space>
                </Card>
              </Col>

              <Col span={16}>
                <Card title={chartTitle || '图表预览'}>
                  <ChartComponent />
                </Card>
              </Col>
            </Row>
          </TabPane>

          <TabPane tab="已保存图表" key="saved">
            <Row gutter={16}>
              {savedCharts.map((chart) => (
                <Col span={8} key={chart.id}>
                  <Card
                    title={chart.title}
                    actions={[
                      <Button type="link" onClick={() => loadChart(chart)}>加载</Button>,
                      <Button type="link" danger onClick={() => deleteChart(chart.id)}>删除</Button>
                    ]}
                  >
                    <div className="text-sm text-gray-600 mb-2">
                      类型: {chart.chart_type}<br/>
                      创建时间: {new Date(chart.created_at).toLocaleDateString()}
                    </div>
                  </Card>
                </Col>
              ))}
            </Row>
          </TabPane>

          <TabPane tab="模板库" key="templates">
            <Row gutter={16}>
              <Col span={8}>
                <Card
                  title="年度发表趋势"
                  hoverable
                  onClick={() => {
                    setChartType('line');
                    setChartTitle('年度发表趋势');
                    setXLabel('年份');
                    setYLabel('发表数量');
                    loadSampleData();
                  }}
                >
                  <LineChartOutlined className="text-4xl text-blue-500" />
                  <p className="mt-2">展示年度文献发表数量变化</p>
                </Card>
              </Col>
              <Col span={8}>
                <Card
                  title="研究领域分布"
                  hoverable
                  onClick={() => {
                    setChartType('pie');
                    setChartTitle('研究领域分布');
                    loadSampleData();
                  }}
                >
                  <PieChartOutlined className="text-4xl text-green-500" />
                  <p className="mt-2">展示不同研究领域的占比</p>
                </Card>
              </Col>
              <Col span={8}>
                <Card
                  title="影响因子对比"
                  hoverable
                  onClick={() => {
                    setChartType('bar');
                    setChartTitle('期刊影响因子对比');
                    setXLabel('期刊');
                    setYLabel('影响因子');
                    loadSampleData();
                  }}
                >
                  <BarChartOutlined className="text-4xl text-purple-500" />
                  <p className="mt-2">对比不同期刊的影响因子</p>
                </Card>
              </Col>
            </Row>
          </TabPane>
        </Tabs>
      </div>
    </div>
  );
};

export default ResearchTools;