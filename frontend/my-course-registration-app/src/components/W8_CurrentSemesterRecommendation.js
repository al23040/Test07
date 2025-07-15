import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { fetchCurrentSemesterRecommendation, fetchAllSubjects, fetchUserTakenCourses } from '../api';
import './W8_CurrentSemesterRecommendation.css';

const W8_CurrentSemesterRecommendation = () => {
  const [recommendationData, setRecommendationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const userId = parseInt(localStorage.getItem('user_id'), 10);
  
  useEffect(() => {
    if (!userId) {
      alert("ユーザーIDが見つかりません。ログインしてください。");
      navigate('/login');
      return;
    }

    const userConditions = {
      max_credits_per_semester: 20,
      exclude_field: 'none'
    };

    const getRecommendation = async () => {
      setLoading(true);
      try {
        const completedCourses = await fetchUserTakenCourses(userId);
        const allCourses = await fetchAllSubjects();
        const data = await fetchCurrentSemesterRecommendation(userId, userConditions, completedCourses, allCourses);
        setRecommendationData(data);
      } catch (err) {
        console.error(err.response?.data || err.message);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    getRecommendation();
  }, [userId, navigate]);

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>今学期のおすすめ科目を計算中です...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p>エラー: {error.message}</p>
      </div>
    );
  }

  if (!recommendationData) {
    return <p>おすすめの履修情報はありません。</p>;
  }

  return (
    <div className="recommendation-container">
      <header className="recommendation-header">
        <h1>{recommendationData.summary?.target_semester || '今学期'}のおすすめ履修</h1>
        <p className="summary-message">{recommendationData.summary?.message}</p>
        <div className="summary-meta">
          <span>推奨単位数: <strong>{recommendationData.total_credits}</strong></span>
        </div>
      </header>

      <div className="recommendation-body">

        <section className="course-section">
          <h2>推奨科目リスト</h2>
          {recommendationData.recommended_courses && recommendationData.recommended_courses.length > 0 ? (
            <ul className="course-list">
              {recommendationData.recommended_courses.map((course) => (
                <li key={course.course_id} className="course-item">
                  <div className="course-info">
                    <span className="course-name">{course.name}</span>
                    <span className="course-details">{course.category} / {course.credits}単位</span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>推奨科目はありません。</p>
          )}
        </section>

        <section className="course-section">
          <h2>代替科目リスト</h2>
          <p className="section-description">推奨科目が履修できない場合に、代わりに履修を検討できる科目です。</p>
          {recommendationData.alternative_courses && recommendationData.alternative_courses.length > 0 ? (
            <ul className="course-list alternative">
              {recommendationData.alternative_courses.map((course) => (
                <li key={course.course_id} className="course-item">
                   <div className="course-info">
                    <span className="course-name">{course.name}</span>
                    <span className="course-details">{course.category} / {course.credits}単位</span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p>代替科目はありません。</p>
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

