// frontend/my-course-registration-app/src/components/W7_FourYearPatternList.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
// 必要なAPI関数をインポート
import { fetchFourYearPatterns, fetchAllSubjects, fetchUserTakenCourses } from '../api';
import './W7_FourYearPatternList.css';

const W7_FourYearPatternList = () => {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ユーザーIDと条件を仮で設定（本来は認証情報やContextから取得します）
  const userId = 1;
  const userConditions = {
    // 例: { "max_credits_per_semester": 20, "exclude_field": "humanities" }
  };

  useEffect(() => {
    const getPatterns = async () => {
      setLoading(true);
      try {
        // C5から科目データを取得
        const completedCourses = await fetchUserTakenCourses(userId);
        const allCourses = await fetchAllSubjects();
        
        // C4 APIを呼び出す際に取得したデータを渡す
        const data = await fetchFourYearPatterns(userId, userConditions, completedCourses, allCourses);
        setPatterns(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getPatterns();
    // userConditionsはオブジェクトなので、JSON.stringifyして比較する
  }, [userId, JSON.stringify(userConditions)]); 

  if (loading) return <div className="loading-container"><div className="loader"></div><p>履修パターンを生成中...</p></div>;
  if (error) return <div className="error-container"><p>エラーが発生しました: {error.message}</p></div>;
  
  return (
    <div className="four-year-pattern-list">
      <h2>4年間の履修パターン</h2>
      {patterns && patterns.length > 0 ? (
        <ul>
          {patterns.map((pattern) => (
            <li key={pattern.id}>
              <Link to={`/patterns/${pattern.id}`}>
                <h3>{pattern.name}</h3>
                <p>{pattern.description}</p>
                <span>総単位数: {pattern.totalUnits}</span>
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>表示できる履修パターンがありません。</p>
      )}
    </div>
  );
};

export default W7_FourYearPatternList;
