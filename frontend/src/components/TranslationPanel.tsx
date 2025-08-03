import React, { useState } from 'react';
import { Globe, Copy, Check, X, Loader2 } from 'lucide-react';
import { useAppSelector } from '../store/hooks';

interface TranslationPanelProps {
  literature: {
    title: string;
    abstract?: string;
    keywords?: string[];
    authors?: string[];
    journal?: string;
  };
  onClose: () => void;
}

interface TranslationResult {
  title: string;
  abstract?: string;
  keywords?: string[];
  authors?: string[];
  journal?: string;
  original_data: any;
}

const TranslationPanel: React.FC<TranslationPanelProps> = ({ literature, onClose }) => {
  const [translating, setTranslating] = useState(false);
  const [translation, setTranslation] = useState<TranslationResult | null>(null);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const [config, setConfig] = useState<{ baidu_configured: boolean } | null>(null);

  const { user } = useAppSelector(state => state.auth);

  React.useEffect(() => {
    checkTranslationConfig();
  }, []);

  const checkTranslationConfig = async () => {
    try {
      const response = await fetch('/api/literature/translate/config/');
      const data = await response.json();
      if (data.success) {
        setConfig(data.data);
      }
    } catch (err) {
      console.error('检查翻译配置失败:', err);
    }
  };

  const translateLiterature = async () => {
    setTranslating(true);
    setError('');

    try {
      const response = await fetch('/api/literature/translate/literature/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user?.token}`,
        },
        body: JSON.stringify({
          literature,
          target_lang: 'zh',
        }),
      });

      const data = await response.json();

      if (data.success) {
        setTranslation(data.data);
      } else {
        setError(data.message || '翻译失败');
      }
    } catch (err) {
      setError('网络错误，请重试');
    } finally {
      setTranslating(false);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  const renderSection = (title: string, content: string | string[] | undefined, original?: string | string[]) => {
    if (!content) return null;

    const displayContent = Array.isArray(content) ? content.join(', ') : content;
    const displayOriginal = Array.isArray(original) ? original.join(', ') : original;

    return (
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="font-semibold text-gray-700">{title}</h4>
          <button
            onClick={() => copyToClipboard(displayContent)}
            className="p-1 text-gray-500 hover:text-gray-700"
            title="复制翻译结果"
          >
            {copied ? <Check size={16} className="text-green-500" /> : <Copy size={16} />}
          </button>
        </div>
        <div className="bg-blue-50 p-3 rounded-lg">
          <p className="text-gray-800">{displayContent}</p>
        </div>
        {displayOriginal && displayOriginal !== displayContent && (
          <div className="mt-2 text-sm text-gray-500">
            <p className="font-medium">原文:</p>
            <p>{displayOriginal}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] flex flex-col">
        {/* 头部 */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center gap-2">
            <Globe size={24} className="text-blue-500" />
            <h2 className="text-xl font-bold text-gray-800">文献翻译</h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X size={24} />
          </button>
        </div>

        {/* 内容区域 */}
        <div className="flex-1 overflow-y-auto p-4">
          {/* 配置状态 */}
          {config && !config.baidu_configured && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                ⚠️ 翻译服务未配置，将使用测试翻译模式。请联系管理员配置百度翻译API。
              </p>
            </div>
          )}

          {/* 原文预览 */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">原文预览</h3>
            <div className="bg-gray-50 p-4 rounded-lg">
              {renderSection('标题', literature.title)}
              {literature.abstract && renderSection('摘要', literature.abstract)}
              {literature.journal && renderSection('期刊', literature.journal)}
              {literature.authors && literature.authors.length > 0 && renderSection('作者', literature.authors)}
              {literature.keywords && literature.keywords.length > 0 && renderSection('关键词', literature.keywords)}
            </div>
          </div>

          {/* 翻译按钮 */}
          {!translation && (
            <div className="text-center mb-6">
              <button
                onClick={translateLiterature}
                disabled={translating}
                className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 mx-auto"
              >
                {translating ? (
                  <>
                    <Loader2 size={20} className="animate-spin" />
                    翻译中...
                  </>
                ) : (
                  <>
                    <Globe size={20} />
                    开始翻译
                  </>
                )}
              </button>
            </div>
          )}

          {/* 错误信息 */}
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {/* 翻译结果 */}
          {translation && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">翻译结果</h3>
              <div className="bg-green-50 p-4 rounded-lg">
                {renderSection('标题', translation.title, literature.title)}
                {translation.abstract && renderSection('摘要', translation.abstract, literature.abstract)}
                {translation.journal && renderSection('期刊', translation.journal, literature.journal)}
                {translation.authors && translation.authors.length > 0 && renderSection('作者', translation.authors, literature.authors)}
                {translation.keywords && translation.keywords.length > 0 && renderSection('关键词', translation.keywords, literature.keywords)}
              </div>
            </div>
          )}
        </div>

        {/* 底部操作区 */}
        <div className="p-4 border-t bg-gray-50 flex items-center justify-end gap-2">
          {translation && (
            <>
              <button
                onClick={() => {
                  const allText = [
                    `标题: ${translation.title}`,
                    `摘要: ${translation.abstract || '无'}`,
                    `期刊: ${translation.journal || '无'}`,
                    `作者: ${translation.authors?.join(', ') || '无'}`,
                    `关键词: ${translation.keywords?.join(', ') || '无'}`,
                  ].join('\n\n');
                  copyToClipboard(allText);
                }}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 flex items-center gap-2"
              >
                {copied ? <Check size={16} /> : <Copy size={16} />}
                {copied ? '已复制' : '复制全部'}
              </button>
              <button
                onClick={() => setTranslation(null)}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100"
              >
                重新翻译
              </button>
            </>
          )}
          <button
            onClick={onClose}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  );
};

export default TranslationPanel;