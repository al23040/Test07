// src/components/CurrentSemesterRecommendation.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Linkをインポート
import { fetchCurrentSemesterRecommendation } from '../api';
import './CurrentSemesterRecommendation.css';

const CurrentSemesterRecommendation = () => {
  const [recommendationData, setRecommendationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 仮の現在の学年。実際にはユーザー情報などから取得します。
  const currentStudentYear = 1; // ここで学年を調整してテストできます（1～4）

  useEffect(() => {
    const getRecommendation = async () => {
      try {
        const data = await fetchCurrentSemesterRecommendation(currentStudentYear);
        setRecommendationData(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getRecommendation();
  }, [currentStudentYear]);

  if (loading) {
    return <div className="loading">おすすめ履修データをロード中...</div>;
  }

  if (error) {
    return <div className="error">データのロードに失敗しました: {error.message}</div>;
  }

  if (!recommendationData) {
    return <div className="no-data">おすすめ履修データが見つかりませんでした。</div>;
  }

  const days = ['月', '火', '水', '木', '金'];
  const periods = ['1限', '2限', '3限', '4限', '5限'];

  return (
    <div className="current-semester-recommendation">
      <h2>今学期のおすすめ履修登録</h2>
      <h3>{recommendationData.year}年生 {recommendationData.semester}</h3>
      <p>総単位数: {recommendationData.totalUnits}</p>
      <p>残り単位数: {recommendationData.remainingUnits}</p>
      <p>基本情報技術者試験内容習得率: {recommendationData.basicTechExamCompletionRate}%</p>

      <h4>おすすめ科目:</h4>
      {recommendationData.recommendedSubjects.length > 0 ? (
        <ul>
          {recommendationData.recommendedSubjects.map(subject => (
            <li key={subject.id}>{subject.name} ({subject.units}単位)</li>
          ))}
        </ul>
      ) : (
        <p>おすすめ科目は現在ありません。</p>
      )}

      {recommendationData.currentSemesterSchedule && (
        <div className="timetable-section">
          <h4>今学期の時間割</h4>
          <table className="timetable" border="1">
            <thead>
              <tr>
                <th>時間</th>
                {days.map(day => <th key={day}>{day}</th>)}
              </tr>
            </thead>
            <tbody>
              {periods.map(period => (
                <tr key={period}>
                  <td>{period}</td>
                  {days.map(day => (
                    <td key={`${day}-${period}`}>
                      {recommendationData.currentSemesterSchedule[day] && recommendationData.currentSemesterSchedule[day][period]
                        ? recommendationData.currentSemesterSchedule[day][period]
                        : ''}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p className="notes">{recommendationData.notes}</p>

      {/* 「次へ」ボタンを追加 */}
      <Link to="/patterns" className="next-button">履修パターンを見る</Link>
    </div>
  );
};

export default CurrentSemesterRecommendation;