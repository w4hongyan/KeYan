import React, { useState, useEffect } from 'react';
import { Search, Download, Eye, X, Filter, ChevronDown } from 'lucide-react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { addLiterature } from '../store/slices/literatureSlice';

interface PubMedArticle {
  pmid: string;
  title: string;
  authors: string[];
  abstract: string;
  journal: string;
  pub_year: number;
  doi: string;
  keywords: string[];
  full_text_url?: string;
}

interface PubMedSearchProps {
  onClose: () => void;
  onImport: (articles: PubMedArticle[]) => void;
}

const PubMedSearch: React.FC<PubMedSearchProps> = ({ onClose, onImport }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('general');
  const [maxResults, setMaxResults] = useState(20);
  const [articles, setArticles] = useState<PubMedArticle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedArticles, setSelectedArticles] = useState<Set<string>>(new Set());
  const [showFilters, setShowFilters] = useState(false);
  
  const dispatch = useAppDispatch();
  const { user } = useAppSelector(state => state.auth);

  const searchPubMed = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const params = new URLSearchParams({
        query: searchQuery,
        max_results: maxResults.toString(),
        type: searchType
      });
      
      const response = await fetch(`/api/literature/pubmed/search/?${params}`);
      const data = await response.json();
      
      if (data.success) {
        setArticles(data.data.results);
      } else {
        setError(data.message || '搜索失败');
      }
    } catch (err) {
      setError('网络错误，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      searchPubMed();
    }
  };

  const toggleArticleSelection = (pmid: string) => {
    const newSelected = new Set(selectedArticles);
    if (newSelected.has(pmid)) {
      newSelected.delete(pmid);
    } else {
      newSelected.add(pmid);
    }
    setSelectedArticles(newSelected);
  };

  const handleImportSelected = () => {
    const selected = articles.filter(article => selectedArticles.has(article.pmid));
    onImport(selected);
    setSelectedArticles(new Set());
  };

  const handleImportAll = () => {
    onImport(articles);
    setSelectedArticles(new Set());
  };

  const viewFullText = (url?: string) => {
    if (url) {
      window.open(url, '_blank');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-6xl max-h-[90vh] flex flex-col">
        {/* 头部 */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-xl font-bold text-gray-800">PubMed文献搜索</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X size={24} />
          </button>
        </div>

        {/* 搜索区域 */}
        <div className="p-4 border-b">
          <div className="flex gap-2 mb-3">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="输入搜索关键词..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="px-3 py-2 border rounded-lg hover:bg-gray-50 flex items-center gap-2"
            >
              <Filter size={16} />
              筛选
              <ChevronDown size={16} className={showFilters ? 'rotate-180' : ''} />
            </button>
            <button
              onClick={searchPubMed}
              disabled={loading || !searchQuery.trim()}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
            >
              {loading ? '搜索中...' : '搜索'}
            </button>
          </div>

          {showFilters && (
            <div className="flex gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">搜索类型</label>
                <select
                  value={searchType}
                  onChange={(e) => setSearchType(e.target.value)}
                  className="border rounded px-2 py-1 text-sm"
                >
                  <option value="general">通用搜索</option>
                  <option value="author">作者搜索</option>
                  <option value="journal">期刊搜索</option>
                  <option value="doi">DOI搜索</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">结果数量</label>
                <select
                  value={maxResults}
                  onChange={(e) => setMaxResults(Number(e.target.value))}
                  className="border rounded px-2 py-1 text-sm"
                >
                  <option value={10}>10条</option>
                  <option value={20}>20条</option>
                  <option value={50}>50条</option>
                  <option value={100}>100条</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* 错误信息 */}
        {error && (
          <div className="p-4 bg-red-50 border-b">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* 结果区域 */}
        <div className="flex-1 overflow-y-auto">
          {articles.length === 0 && !loading && (
            <div className="text-center py-12 text-gray-500">
              <Search size={48} className="mx-auto mb-4 text-gray-300" />
              <p>请输入关键词搜索PubMed文献</p>
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
              <p className="mt-2 text-gray-500">正在搜索文献...</p>
            </div>
          )}

          {articles.map((article) => (
            <div key={article.pmid} className="p-4 border-b hover:bg-gray-50">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-start gap-3">
                    <input
                      type="checkbox"
                      checked={selectedArticles.has(article.pmid)}
                      onChange={() => toggleArticleSelection(article.pmid)}
                      className="mt-1"
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-800 mb-1">{article.title}</h3>
                      <p className="text-sm text-gray-600 mb-1">
                        {article.authors.join(', ')}
                      </p>
                      <p className="text-sm text-gray-500 mb-1">
                        {article.journal} • {article.pub_year}
                      </p>
                      {article.abstract && (
                        <p className="text-sm text-gray-700 mb-2 line-clamp-3">
                          {article.abstract}
                        </p>
                      )}
                      <div className="flex gap-2 text-xs">
                        <span className="text-gray-500">PMID: {article.pmid}</span>
                        {article.doi && (
                          <span className="text-blue-500">DOI: {article.doi}</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 ml-4">
                  {article.full_text_url && (
                    <button
                      onClick={() => viewFullText(article.full_text_url)}
                      className="p-2 text-blue-500 hover:bg-blue-50 rounded"
                      title="查看全文"
                    >
                      <Eye size={16} />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* 底部操作区 */}
        {articles.length > 0 && (
          <div className="p-4 border-t bg-gray-50 flex items-center justify-between">
            <div className="text-sm text-gray-600">
              已选择 {selectedArticles.size} 篇文献
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleImportAll}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
              >
                导入全部
              </button>
              <button
                onClick={handleImportSelected}
                disabled={selectedArticles.size === 0}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                导入选中 ({selectedArticles.size})
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PubMedSearch;