// src/components/CurrentSemesterRecommendation.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchCurrentSemesterRecommendation } from '../api'; // 修正されたapi.jsからインポート
import './CurrentSemesterRecommendation.css';

const CurrentSemesterRecommendation = () => {
  const [recommendationData, setRecommendationData] = useState(null);
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
    const getRecommendation = async () => {
      try {
        // C4 APIを呼び出す際にuserIdとconditionsを渡す
        const data = await fetchCurrentSemesterRecommendation(userId, userConditions);
        setRecommendationData(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getRecommendation();
  }, [userId, JSON.stringify(userConditions)]); // conditionsオブジェクトの変更を検知するためにstringify

  if (loading) {
    return <div className="loading">おすすめ履修データをロード中...</div>;
  }

  if (error) {
    return <div className="error">データのロードに失敗しました: {error.message}</div>;
  }

  if (!recommendationData) {
    return <div className="no-data">おすすめ履修データが見つかりませんでした。</div>;
  }

  // ... (既存のJSXレンダリングロジックは変わらないはず) ...
  const days = ['月', '火', '水', '木', '金'];
  const periods = ['1限', '2限', '3限', '4限', '5限'];

  return (
    <div className="current-semester-recommendation">
      <h2>今学期のおすすめ履修</h2>
      {recommendationData.semesterInfo && (
        <p><strong>{recommendationData.semesterInfo}</strong></p>
      )}
      {recommendationData.totalCredits && (
        <p>現在の総取得単位数: {recommendationData.totalCredits}</p>
      )}
      {recommendationData.remainingRequirements && (
        <div>
          <h4>残りの卒業要件（目安）:</h4>
          <ul>
            {Object.entries(recommendationData.remainingRequirements).map(([category, reqs]) => (
              <li key={category}>
                {category}: {Object.entries(reqs).map(([type, value]) => (
                  <span key={type}>{type}: {value}単位 </span>
                ))}
              </li>
            ))}
          </ul>
        </div>
      )}

      <h3>推奨科目:</h3>
      {recommendationData.recommendedSubjects && recommendationData.recommendedSubjects.length > 0 ? (
        <ul>
          {recommendationData.recommendedSubjects.map(subject => (
            <li key={subject.id}>{subject.name} ({subject.units}単位) {subject.time_slot ? `[${subject.day_of_week} ${subject.time_slot}]` : ''}</li>
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