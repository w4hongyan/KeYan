import React, { useRef, useEffect } from 'react';
import { Editor } from '@tinymce/tinymce-react';
import { message } from 'antd';

interface RichTextEditorProps {
  value?: string;
  onChange?: (content: string) => void;
  height?: number;
  placeholder?: string;
  disabled?: boolean;
}

const RichTextEditor: React.FC<RichTextEditorProps> = ({
  value,
  onChange,
  height = 400,
  placeholder = '请输入内容...',
  disabled = false,
}) => {
  const editorRef = useRef<any>(null);

  const handleEditorChange = (content: string) => {
    if (onChange) {
      onChange(content);
    }
  };

  const handleImageUpload = (blobInfo: any, progress: (percent: number) => void) => {
    return new Promise<string>((resolve, reject) => {
      const formData = new FormData();
      formData.append('file', blobInfo.blob(), blobInfo.filename());

      fetch('/api/upload/image/', {
        method: 'POST',
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          if (data.success && data.url) {
            resolve(data.url);
          } else {
            reject(data.message || '上传失败');
          }
        })
        .catch(error => {
          reject('上传失败');
        });
    });
  };

  return (
    <Editor
      apiKey="your-tinymce-api-key" // 需要替换为实际的API key
      onInit={(_evt, editor) => {
        editorRef.current = editor;
      }}
      value={value}
      onEditorChange={handleEditorChange}
      init={{
        height,
        placeholder,
        menubar: false,
        plugins: [
          'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
          'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
          'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
        ],
        toolbar: 'undo redo | blocks | ' +
          'bold italic forecolor | alignleft aligncenter ' +
          'alignright alignjustify | bullist numlist outdent indent | ' +
          'image link | removeformat | help',
        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
        images_upload_handler: handleImageUpload,
        images_upload_url: '/api/upload/image/',
        automatic_uploads: true,
        file_picker_types: 'image',
        language: 'zh_CN',
        branding: false,
        resize: false,
        readonly: disabled,
      }}
    />
  );
};

export default RichTextEditor;