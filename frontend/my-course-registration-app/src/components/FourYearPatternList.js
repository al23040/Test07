// src/components/FourYearPatternList.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchFourYearPatterns } from '../api';
import './FourYearPatternList.css'; // 必要に応じてCSSファイルを作成

const FourYearPatternList = () => {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getPatterns = async () => {
      try {
        // patternIdなしで呼び出し、概要リストを取得
        const data = await fetchFourYearPatterns();
        setPatterns(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getPatterns();
  }, []);

  if (loading) {
    return <div className="loading">履修パターンをロード中...</div>;
  }

  if (error) {
    return <div className="error">データのロードに失敗しました: {error.message}</div>;
  }

  if (!patterns || patterns.length === 0) {
    return <div className="no-data">利用可能な履修パターンが見つかりませんでした。</div>;
  }

  return (
    <div className="four-year-pattern-list">
      <h2>4年間の履修登録パターン候補</h2>
      <div className="pattern-cards">
        {patterns.map(pattern => (
          <div key={pattern.id} className="pattern-card">
            <h3>{pattern.name}</h3> {/* ここが「パターン1」などの通し番号になります */}
            <p>{pattern.description}</p>
            <p>総取得単位数: {pattern.totalUnits}</p>
            <Link to={`/patterns/${pattern.id}`} className="detail-link">詳細を見る</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FourYearPatternList;