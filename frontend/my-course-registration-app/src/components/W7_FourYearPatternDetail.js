// src/components/W7_FourYearPatternDetail.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchFourYearPatterns } from '../api';
import './W7_FourYearPatternDetail.css';

const W7_FourYearPatternDetail = () => {
  const { patternId } = useParams();
  const [patternDetail, setPatternDetail] = useState(null);
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
    const getPatternDetail = async () => {
      if (!patternId) {
        setError(new Error("パターンIDが指定されていません。"));
        setLoading(false);
        return;
      }
      try {
        // 全パターンを取得し、その中からpatternIdに一致するものを探す
        // より効率的なのは、C4に個別のパターン詳細を取得するAPIを追加すること
        const allPatterns = await fetchFourYearPatterns(userId, userConditions);
        const detail = allPatterns.find(p => p.id === patternId);
        if (detail) {
          setPatternDetail(detail);
        } else {
          setError(new Error("指定されたパターンが見つかりませんでした。"));
        }
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getPatternDetail();
  }, [patternId, userId, JSON.stringify(userConditions)]);

  if (loading) {
    return <div className="loading">履修パターン詳細をロード中...</div>;
  }

  if (error) {
    return <div className="error">データのロードに失敗しました: {error.message}</div>;
  }

  if (!patternDetail) {
    return <div className="no-data">履修パターン詳細が見つかりませんでした。</div>;
  }

  const days = ['月', '火', '水', '木', '金'];
  // 時間割の時限は、取得したデータに合わせて調整
  // 現状のC4出力では '1限', '2限' の形式なので、それに合わせる
  const periods = ['1限', '2限', '3限', '4限', '5限'];


  return (
    <div className="four-year-pattern-detail">
      <h2>{patternDetail.name} の詳細</h2>
      <p className="description">{patternDetail.description}</p>
      <p className="total-units">総取得単位数: {patternDetail.totalUnits}</p>

      <h3>4年間の時間割</h3>
      {patternDetail.semesters.map(semester => (
        <div key={`${semester.year}-${semester.semester}`} className="semester-schedule">
          <h4>{semester.year}年生 {semester.semester}</h4>
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
                      {/* C4からのデータはオブジェクトのvalueとして科目名が来る想定 */}
                      {semester.schedule[day] && semester.schedule[day][period]
                        ? semester.schedule[day][period]
                        : ''}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <p>この学期で取得予定の単位数: {semester.totalCredits}</p>
        </div>
      ))}
      <Link to="/patterns" className="back-button">
        全パターンに戻る
      </Link>
    </div>
  );
};

export default W7_FourYearPatternDetail;