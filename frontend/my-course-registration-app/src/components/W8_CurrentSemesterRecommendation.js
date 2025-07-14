// src/components/W8_CurrentSemesterRecommendation.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
// 必要なAPI関数をインポート
import { fetchCurrentSemesterRecommendation, fetchAllSubjects, fetchUserTakenCourses } from '../api';
import './W8_CurrentSemesterRecommendation.css';

const W8_CurrentSemesterRecommendation = () => {
  const [recommendationData, setRecommendationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // ユーザーIDと条件を仮で設定します。
  // 本来はログイン状態などから動的に取得する想定です。
  const userId = 1; 
  const userConditions = {
    // 例: 現在の学年や学期などを指定
    // "current_year": 1,
    // "current_semester": "前期"
  };

  useEffect(() => {
    const getRecommendation = async () => {
      setLoading(true); // データ取得開始時にローディング状態に設定
      try {
        // C5から履修済み科目と全科目リストを取得
        const completedCourses = await fetchUserTakenCourses(userId);
        const allCourses = await fetchAllSubjects(); 

        // C4 APIを呼び出して、今学期のおすすめ履修データを取得
        const data = await fetchCurrentSemesterRecommendation(userId, userConditions, completedCourses, allCourses);
        setRecommendationData(data);
      } catch (err) {
        setError(err); // エラーが発生したらエラー情報を設定
      } finally {
        setLoading(false); // 処理が完了したらローディング状態を解除
      }
    };

    getRecommendation();
    // userConditionsはオブジェクトのため、JSON文字列に変換して依存配列に渡します
  }, [userId, JSON.stringify(userConditions)]);

  // ローディング中の表示
  if (loading) {
    return (
      <div className="loading-container">
        <div className="loader"></div>
        <p>あなたの状況を分析し、最適な履修プランを計算しています...</p>
      </div>
    );
  }

  // エラー発生時の表示
  if (error) {
    return (
      <div className="error-container">
        <p>エラーが発生しました: {error.message}</p>
        <p>時間をおいて再度お試しください。</p>
      </div>
    );
  }

  // データがない場合の表示
  if (!recommendationData) {
    return <p>表示できるおすすめの履修情報がありません。</p>;
  }

  return (
    <div className="recommendation-container">
      <header className="recommendation-header">
        <h1>{recommendationData.summary.target_semester}のおすすめ履修</h1>
        <p className="summary-message">{recommendationData.summary.message}</p>
        <div className="summary-meta">
          <span>合計単位数: <strong>{recommendationData.total_credits}</strong></span>
        </div>
      </header>

      <div className="recommendation-body">
        <section className="course-section">
          <h2>推奨科目リスト</h2>
          {recommendationData.recommended_courses && recommendationData.recommended_courses.length > 0 ? (
            <ul className="course-list">
              {recommendationData.recommended_courses.map((course) => (
                <li key={course.course_id} className="course-item">
                  <Link to={`/courses/${course.course_id}`} className="course-link">
                    <span className="course-name">{course.name}</span>
                    <span className="course-credits">{course.credits}単位</span>
                  </Link>
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
                    <span className="course-name">{course.name}</span>
                    <span className="course-credits">{course.credits}単位</span>
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
        <Link to="/conditions" className="btn-link">条件を再設定する</Link>
      </footer>
    </div>
  );
};

export default W8_CurrentSemesterRecommendation;