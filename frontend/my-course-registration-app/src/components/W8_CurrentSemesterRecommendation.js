// src/components/W8_CurrentSemesterRecommendation.js

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchCurrentSemesterRecommendation } from '../api'; // API関数
import './W8_CurrentSemesterRecommendation.css';
import axios from 'axios';

// --- Contextをインポート ---
import { useAuth } from '../context/AuthContext';
import { useConditions } from '../context/ConditionsContext';

const W8_CurrentSemesterRecommendation = () => {
  const [recommendationData, setRecommendationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- Contextから必要なデータを取得 ---
  const { userId } = useAuth();
  const { conditions } = useConditions();
  
  const calculateTotalCredits = (subjects) => {
  if (!subjects) return 0;
  return subjects.reduce((total, subject) => total + subject.units, 0);
  };

  useEffect(() => {
    // 必要なデータが揃うまで待つ
    if (!userId) {
      return;
    }

    const getRecommendation = async () => {
      setLoading(true);
      setError(null);
      try {
        // ContextのデータをAPI関数に渡す
        const dataToSend = {
          userId: userId,
          conditions: conditions,
        };
        const resCompleted = await axios.post(`/api/c7/user_courses/${userId}`, dataToSend);
        const resAvailable = await axios.post(`/api/c7/user_courses/${userId}`, dataToSend);
        const completedCourses = resCompleted.data.completed_courses;
        const availableCourses = resAvailable.data.available_courses;
        const data = await fetchCurrentSemesterRecommendation(
          userId,
          conditions,
          completedCourses,
          availableCourses
        );
        setRecommendationData(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    getRecommendation();
    // 依存配列にContextの値を追加
  }, [userId, conditions]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>今学期のおすすめ科目を計算中です...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error-container"><p>エラー: {error.message}</p></div>;
  }

  if (!recommendationData) {
    return <p>おすすめの履修情報はありません。</p>;
  }

 return (
    <div className="recommendation-container">
      <header className="recommendation-header">
        <h1>{recommendationData.year}年度 {recommendationData.semester}のおすすめ履修</h1>
        <p className="summary-message">{recommendationData.notes}</p>
        <div className="summary-meta">
          <span>推奨単位数: <strong>{calculateTotalCredits(recommendationData.recommendedSubjects)}</strong></span>
        </div>
      </header>

      <div className="recommendation-body">

        <section className="course-section">
          <h2>推奨科目リスト</h2>
          {recommendationData.recommendedSubjects && recommendationData.recommendedSubjects.length > 0 ? (
            <ul className="course-list">
              {recommendationData.recommendedSubjects.map((course) => (
                <li key={course.id} className="course-item">
                  <div className="course-info">
                    <span className="course-name">{course.name}</span>
                    <span className="course-details">{course.category} / {course.units}単位</span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>推奨科目はありません。</p>
          )}
        </section>
      </div>
      <footer className="recommendation-footer">
        <p>この情報は、あなたの履修状況と設定に基づいて生成されています。</p>
        <Link to="/patterns" className="btn-link">4年間の履修パターンを見る</Link>
      </footer>
    </div>
  );
};

export default W8_CurrentSemesterRecommendation;