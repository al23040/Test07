// src/components/W7_FourYearPatternList.js

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchFourYearPatterns } from '../api'; // API関数
import './W7_FourYearPatternList.css';
import axios from 'axios';

// --- Contextをインポート ---
import { useAuth } from '../context/AuthContext';
import { useConditions } from '../context/ConditionsContext';

const W7_FourYearPatternList = () => {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Contextから必要なデータを取得 ---
  const { userId } = useAuth();
  const { conditions } = useConditions();


  useEffect(() => {
    // ユーザー情報や科目情報がまだ読み込まれていない場合は、処理を開始しない
    if (!userId) {
      return;
    }

    const getPatterns = async () => {
      setLoading(true);
      setError(null);
      try {
        // Contextから取得したデータをAPI関数に渡す
        const dataToSend = {
          userId: userId,
          conditions: conditions,
        };
        const allCourses = await axios.post(`/api/c7/user_courses/${userId}`, dataToSend);
        const completedCourses = await axios.post(`/api/c7/user_courses/${userId}`, dataToSend);
        const data = await fetchFourYearPatterns(
          userId,
          conditions,
          completedCourses,
          allCourses
        );
        setPatterns(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    getPatterns();
    // 依存配列にContextから取得した値を追加
  }, [userId, conditions]);

  // Contextのデータ読み込み中 + このコンポーネントのデータ読み込み中の両方を考慮
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