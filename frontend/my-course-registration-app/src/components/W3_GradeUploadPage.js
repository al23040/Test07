// src/components/W3_GradeUploadPage.js
import React, { useState, useCallback } from 'react';
import './W3_GradeUploadPage.css';
import { useNavigate } from 'react-router-dom';

function GradeUploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFile = useCallback(async (file) => {
    setSelectedFile(file);
    setMessage('');

    if (!file || file.type !== 'application/pdf') {
      setMessage('PDFファイルを選択してください。');
      return;
    }

    try {
      setLoading(true);

      // 本来のAPI通信（本番環境用）
      const formData = new FormData();
      formData.append('file', file);

const response = await fetch('http://localhost:5000/api/upload-pdf', {
  method: 'POST',
  body: formData
});


      if (!response.ok) {
        throw new Error('解析に失敗しました');
      }

      const json = await response.json();

      if (json.courses && json.available_courses && json.credit_data) {
        localStorage.setItem('parsedCourses', JSON.stringify(json.courses));
        localStorage.setItem('availableCourses', JSON.stringify(json.available_courses));
        localStorage.setItem('creditData', JSON.stringify(json.credit_data));
        setMessage('PDFが正常にアップロード・解析されました。');
      } else {
        throw new Error('形式が不正なデータです');
      }

    } catch (error) {
      console.error(error);
      setMessage('PDF解析に失敗しました。');

      // ============================
      // ↓ デバッグ用：ローカルの send_data.json を読み込む
      // ============================
      try {
        const localResponse = await fetch('/send_data.json');
        if (!localResponse.ok) throw new Error('send_data.json 読み込み失敗');
        const localJson = await localResponse.json();

        localStorage.setItem('parsedCourses', JSON.stringify(localJson.courses));
        localStorage.setItem('availableCourses', JSON.stringify(localJson.available_courses));
        localStorage.setItem('creditData', JSON.stringify(localJson.credit_data));

        setMessage('ローカルの send_data.json を読み込みました。');
      } catch (localErr) {
        console.error('ローカルJSON読み込みにも失敗:', localErr);
        setMessage('ローカルのデータ読み込みにも失敗しました。');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    handleFile(file);
  };

  const handleDrop = useCallback((event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    handleFile(file);
  }, [handleFile]);

  const handleDragOver = useCallback((event) => {
    event.preventDefault();
  }, []);

  const handleNext = () => {
    if (selectedFile && localStorage.getItem('parsedCourses')) {
      navigate('/subject-confirmation');
    } else {
      setMessage('PDFファイルをアップロードしてください。');
    }
  };

  return (
    <div className="grade-upload-container">
      <h2>履修登録状況の入力</h2>
      <div className="upload-content">
        <div className="upload-text">成績通知書登録</div>
        <div
          className="upload-section"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="upload-text">ここにPDFファイルをドロップ<br />または</div>
          <label htmlFor="file-input" className="file-input-button"> ファイルを選択する</label>
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="file-input"
          />
        </div>
      </div>
      <div className="next-button-container">
        <button onClick={handleNext} className="next-button" disabled={loading}>
          {loading ? '解析中...' : '次へ'}
        </button>
      </div>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default GradeUploadPage;

