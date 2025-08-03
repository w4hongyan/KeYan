import React from 'react';

interface ErrorDisplayProps {
  error: any;
}

const ErrorDisplay: React.FC<ErrorDisplayProps> = ({ error }) => {
  if (!error) return null;

  // 提取统一格式的错误信息
  const unifiedError = error.response?.data;
  const hasUnifiedError = unifiedError && typeof unifiedError === 'object' && 'success' in unifiedError;

  return (
    <div className="mt-4 p-4 bg-red-50 rounded-lg border border-red-200">
      <h3 className="text-lg font-semibold text-red-700 mb-2">错误详情</h3>
      <div className="space-y-2 text-sm text-gray-700">
        {hasUnifiedError ? (
          <>{            unifiedError.message && (
              <div>
                <span className="font-medium">错误消息:</span> {unifiedError.message}
              </div>
            )          }{            unifiedError.code && (
              <div>
                <span className="font-medium">错误代码:</span> {unifiedError.code}
              </div>
            )          }{            unifiedError.errors && (
              <div>
                <span className="font-medium">详细错误:</span>
                <div className="mt-1 space-y-1">
                  {Object.entries(unifiedError.errors).map(([field, messages]) => (
                    <div key={field} className="pl-2 border-l-2 border-red-300">
                      <span className="font-medium text-red-600">{field}:</span> {Array.isArray(messages) ? messages.join('; ') : messages}
                    </div>
                  ))}
                </div>
              </div>
            )          }</>
        ) : (
          <>{            error.message && (
              <div>
                <span className="font-medium">错误消息:</span> {error.message}
              </div>
            )          }{            error.response && (
              <div>
                <span className="font-medium">状态码:</span> {error.response.status}
              </div>
            )          }{            error.response?.data && (
              <div>
                <span className="font-medium">响应数据:</span>
                <pre className="mt-1 p-2 bg-gray-100 rounded overflow-x-auto text-xs">
                  {JSON.stringify(error.response.data, null, 2)}
                </pre>
              </div>
            )          }</>
        )}
      </div>
    </div>
  );
};

export default ErrorDisplay;