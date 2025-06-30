// src/components/FourYearPatternList.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchFourYearPatterns } from '../api'; // 修正されたapi.jsからインポート
import './FourYearPatternList.css';

const FourYearPatternList = () => {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 仮のユーザーIDと条件。実際にはログイン情報や希望条件入力画面から取得する
  const userId = 12345; // ログインしているユーザーのIDに置き換える
  const userConditions = {
    min_units: 16,
    max_units: 20,
    preferences: ["balanced"],
    avoid_first_period: false,
    preferred_time_slots: [],
    preferred_categories: [],
    preferred_days: [],
    avoided_days: []
  };

  useEffect(() => {
    const getPatterns = async () => {
      try {
        // C4 APIを呼び出す際にuserIdとconditionsを渡す
        // FourYearPatternListは詳細ではなく、パターン概要のリストを期待
        const data = await fetchFourYearPatterns(userId, userConditions);
        setPatterns(data); // dataはパターンの配列を直接含むと想定
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getPatterns();
  }, [userId, JSON.stringify(userConditions)]);

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
            <h3>{pattern.name}</h3>
            <p className="pattern-description">{pattern.description}</p>
            <p className="pattern-total-units">総取得単位数: {pattern.totalUnits}単位</p>
            <Link to={`/patterns/${pattern.id}`} className="view-detail-button">
              詳細を見る
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FourYearPatternList;