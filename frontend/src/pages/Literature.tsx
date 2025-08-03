import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Tag, Avatar, Space, List, Pagination, Modal, Form, Select, message } from 'antd';
import { StarOutlined, DownloadOutlined, ShareAltOutlined, FilterOutlined, BookOutlined, SearchOutlined, GlobalOutlined, ImportOutlined } from '@ant-design/icons';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { literatureAPI } from '../services/api';
import { fetchLiteraturesStart, fetchLiteraturesSuccess, fetchLiteraturesFailure } from '../store/slices/literatureSlice';
import PubMedSearch from '../components/PubMedSearch';
import TranslationPanel from '../components/TranslationPanel';

const { Search } = Input;
const { Option } = Select;

interface Literature {
  id: number;
  title: string;
  abstract: string;
  authors: string[];
  journal: { id: number; name: string };
  pub_year: number;
  doi: string;
  pmid: string;
  keywords: string[];
  rating: number;
  is_favorite: boolean;
}

interface Journal {
  id: number;
  name: string;
  impact_factor: number;
  cas_partition: string;
  jcr_partition: string;
}

const LiteraturePage: React.FC = () => {
  const [journals, setJournals] = useState<Journal[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchText, setSearchText] = useState('');
  const [selectedJournal, setSelectedJournal] = useState<string>('');
  const [selectedYear, setSelectedYear] = useState<string>('');
  const [isSearchModalVisible, setIsSearchModalVisible] = useState(false);
  const [advancedSearchParams, setAdvancedSearchParams] = useState<any>({});
  const [showPubMedSearch, setShowPubMedSearch] = useState(false);
  const [showTranslation, setShowTranslation] = useState(false);
  const [selectedLiteratureForTranslation, setSelectedLiteratureForTranslation] = useState<any>(null);

  const dispatch = useDispatch();
  const user = useSelector((state: RootState) => state.auth.user);
  const { literatures, loading, total } = useSelector((state: RootState) => state.literature);

  useEffect(() => {
    fetchLiteratures();
    fetchJournals();
  }, [currentPage, searchText, selectedJournal, selectedYear, advancedSearchParams]);

  const fetchLiteratures = async () => {
    dispatch(fetchLiteraturesStart());
    try {
      const params: any = {
        page: currentPage,
        search: searchText,
      };

      if (selectedJournal) params.journal = selectedJournal;
      if (selectedYear) params.pub_year = selectedYear;
      // 添加高级搜索参数
      Object.assign(params, advancedSearchParams);

      const response = await literatureAPI.getLiterature(params);
      // 处理API响应格式
      let data = response;
      let total = 0;
      
      if (response && typeof response === 'object') {
        if (response.data && Array.isArray(response.data)) {
          data = response.data;
          total = response.count || response.data.length || 0;
        } else if (Array.isArray(response)) {
          data = response;
          total = response.length;
        } else {
          data = response.data || response.results || response;
          total = response.count || response.total || (Array.isArray(data) ? data.length : 0);
        }
      }
      
      dispatch(fetchLiteraturesSuccess({
        literatures: Array.isArray(data) ? data : [],
        total: total
      }));
    } catch (error) {
      dispatch(fetchLiteraturesFailure());
      message.error('获取文献列表失败');
    }
  };

  const fetchJournals = async () => {
    try {
      // 调用获取期刊列表的API端点
      const response = await literatureAPI.getJournals();
      // 处理API响应格式
      let data = response;
      
      if (response && typeof response === 'object') {
        if (Array.isArray(response)) {
          data = response;
        } else {
          data = response.data || response.results || response || [];
        }
      } else {
        data = [];
      }
      
      setJournals(Array.isArray(data) ? data : []);
    } catch (error) {
      message.error('获取期刊列表失败');
    }
  };

  const handleSearch = (value: string) => {
    setSearchText(value);
    setCurrentPage(1);
    // 清空高级搜索参数
    setAdvancedSearchParams({});
  };

  const handleAdvancedSearchSubmit = (values: any) => {
    // 构建高级搜索参数
    const params: any = {};
    if (values.title) params.title = values.title;
    if (values.authors) params.authors = values.authors;
    if (values.journal) params.journal = values.journal;
    if (values.year_from) params.year_from = values.year_from;
    if (values.year_to) params.year_to = values.year_to;
    if (values.keywords) params.keywords = values.keywords;

    setAdvancedSearchParams(params);
    setCurrentPage(1);
    setIsSearchModalVisible(false);
  };

  const toggleFavorite = async (id: number, isFavorite: boolean) => {
    try {
      await literatureAPI.updateLiterature(id, { is_favorite: !isFavorite });
      // 由于我们使用Redux管理状态，这里应该触发一个action来更新状态
      // 为了简化，我们可以直接重新获取文献列表
      fetchLiteratures();
      message.success(isFavorite ? '已取消收藏' : '收藏成功');
    } catch (error) {
      message.error('操作失败');
    }
  };

  const downloadFullText = async (id: number) => {
    try {
      const response = await literatureAPI.getLiteratureDetail(id);
      // 假设API返回文献的PDF URL
      if (response.data.pdf_url) {
        window.open(response.data.pdf_url, '_blank');
      } else {
        message.error('该文献没有可用的全文');
      }
    } catch (error) {
      message.error('下载失败');
    }
  };

  const shareLiterature = async (id: number) => {
    try {
      const response = await literatureAPI.getLiteratureDetail(id);
      const literature = response.data;
      // 构建分享链接
      const shareUrl = `${window.location.origin}/literature/${id}`;
      // 复制到剪贴板
      navigator.clipboard.writeText(shareUrl);
      message.success('分享链接已复制到剪贴板');
    } catch (error) {
      message.error('分享失败');
    }
  };

  const importFromPubMed = async (pmid: string) => {
    try {
      await literatureAPI.importFromPubMed(pmid);
      message.success('导入成功');
      fetchLiteratures();
    } catch (error) {
      message.error('导入失败');
    }
  };

  const handlePubMedImport = (articles: any[]) => {
    // 这里可以实现批量导入功能
    Promise.all(
      articles.map(article => 
        literatureAPI.createLiterature({
          title: article.title,
          abstract: article.abstract,
          authors: article.authors,
          journal: article.journal,
          pub_year: article.pub_year,
          doi: article.doi,
          pmid: article.pmid,
          keywords: article.keywords,
        })
      )
    ).then(() => {
      message.success(`成功导入 ${articles.length} 篇文献`);
      setShowPubMedSearch(false);
      fetchLiteratures();
    }).catch(() => {
      message.error('导入失败');
    });
  };

  const handleTranslateLiterature = (literature: any) => {
    setSelectedLiteratureForTranslation(literature);
    setShowTranslation(true);
  };

  // 生成年份选项（近10年）
  const yearOptions = Array.from({ length: 10 }, (_, i) => {
    const year = new Date().getFullYear() - i;
    return <Option key={year} value={year.toString()}>{year}</Option>;
  });

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow-sm rounded-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">文献管理</h1>
            <div className="flex gap-2">
              <Button
                type="primary"
                icon={<ImportOutlined />}
                onClick={() => setShowPubMedSearch(true)}
              >
                PubMed导入
              </Button>
              <Button
                type="primary"
                icon={<FilterOutlined />}
                onClick={() => setIsSearchModalVisible(true)}
              >
                高级搜索
              </Button>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <Search
                placeholder="搜索文献标题、作者、关键词..."
                allowClear
                enterButton={<SearchOutlined />}
                size="large"
                onSearch={handleSearch}
                className="flex-1"
              />
            <Select
              placeholder="选择期刊"
              allowClear
              style={{ width: 200 }}
              value={selectedJournal || undefined}
              onChange={(value) => {
                setSelectedJournal(value);
                setCurrentPage(1);
              }}
            >
              {journals.map(journal => (
                <Option key={journal.id} value={journal.id.toString()}>
                  {journal.name} ({journal.impact_factor}) {journal.cas_partition}
                </Option>
              ))}
            </Select>
            <Select
              placeholder="选择年份"
              allowClear
              style={{ width: 120 }}
              value={selectedYear || undefined}
              onChange={(value) => {
                setSelectedYear(value);
                setCurrentPage(1);
              }}
            >
              {yearOptions}
            </Select>
          </div>
        </div>

        <List
          loading={loading}
          dataSource={literatures}
          renderItem={(literature) => (
            <Card key={literature.id} className="mb-4 hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-start gap-4">
                <div className="flex-1">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {literature.title}
                    </h3>
                    <Button
                      type="text"
                      icon={<StarOutlined className={literature.is_favorite ? "text-yellow-400" : ""} />}
                      onClick={() => toggleFavorite(literature.id, literature.is_favorite)}
                    >
                      {literature.is_favorite ? '已收藏' : '收藏'}
                    </Button>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    {(Array.isArray(literature.authors) ? literature.authors.join(', ') : literature.authors)} ({literature.pub_year})
                  </p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    <Tag color="blue">
                    {literature.journal_info?.name || literature.journal?.name || literature.journal}
                  </Tag>
                    {(Array.isArray(literature.keywords) ? literature.keywords : literature.keywords?.split(/[,;；]\s*/))?.map(keyword => (
                      <Tag key={keyword} color="green">
                        {keyword.trim()}
                      </Tag>
                    ))}
                  </div>
                  <p className="text-sm text-gray-600 line-clamp-3 mb-3">
                    {literature.abstract}
                  </p>
                  <div className="flex flex-wrap gap-2 text-xs text-gray-500">
                    {literature.doi && <span>DOI: {literature.doi}</span>}
                    {literature.pmid && <span>PMID: {literature.pmid}</span>}
                  </div>
                </div>
                <div className="flex flex-col gap-2 w-full md:w-40">
                  {literature.rating > 0 && (
                    <div className="bg-yellow-50 rounded-lg p-2 text-center">
                      <div className="text-yellow-500 font-bold text-2xl">{literature.rating}</div>
                      <div className="text-xs text-gray-500">用户评分</div>
                    </div>
                  )}
                  <Button
                    type="primary"
                    size="small"
                    icon={<GlobalOutlined />}
                    block
                    onClick={() => handleTranslateLiterature(literature)}
                  >
                    翻译
                  </Button>
                  <Button
                    type="primary"
                    size="small"
                    icon={<DownloadOutlined />}
                    block
                    onClick={() => downloadFullText(literature.id)}
                  >
                    下载全文
                  </Button>
                  <Button
                    type="default"
                    size="small"
                    icon={<ShareAltOutlined />}
                    block
                    onClick={() => shareLiterature(literature.id)}
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
            showSizeChanger
            pageSizeOptions={['10', '20', '50']}
          />
        </div>
      </div>

      <Modal
        title="高级搜索"
        open={isSearchModalVisible}
        onCancel={() => setIsSearchModalVisible(false)}
        footer={null}
      >
        <Form layout="vertical" onFinish={handleAdvancedSearchSubmit}>
          <Form.Item name="title" label="标题包含">
            <Input placeholder="输入标题关键词" />
          </Form.Item>
          <Form.Item name="authors" label="作者">
            <Input placeholder="输入作者姓名" />
          </Form.Item>
          <Form.Item name="journal" label="期刊">
            <Select placeholder="选择期刊">
              {journals.map(journal => (
                <Option key={journal.id} value={journal.id}>{journal.name}</Option>
              ))}
            </Select>
          </Form.Item>
          <div className="grid grid-cols-2 gap-4">
            <Form.Item name="year_from" label="发表年份从">
              <Select placeholder="选择起始年份">
                {yearOptions}
              </Select>
            </Form.Item>
            <Form.Item name="year_to" label="到">
              <Select placeholder="选择结束年份">
                {yearOptions}
              </Select>
            </Form.Item>
          </div>
          <Form.Item name="keywords" label="关键词">
            <Input placeholder="输入关键词，多个关键词用逗号分隔" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              搜索
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* PubMed搜索弹窗 */}
      {showPubMedSearch && (
        <PubMedSearch
          onClose={() => setShowPubMedSearch(false)}
          onImport={handlePubMedImport}
        />
      )}

      {/* 翻译面板 */}
      {showTranslation && selectedLiteratureForTranslation && (
        <TranslationPanel
          literature={selectedLiteratureForTranslation}
          onClose={() => {
            setShowTranslation(false);
            setSelectedLiteratureForTranslation(null);
          }}
        />
      )}
    </div>
  );
};

export default LiteraturePage;