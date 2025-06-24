// src/components/FourYearPatternDetail.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom'; // Linkをインポート
import { fetchFourYearPatterns } from '../api';
import './FourYearPatternDetail.css'; // 必要に応じてCSSファイルを作成

const FourYearPatternDetail = () => {
  const { patternId } = useParams(); // URLからpatternIdを取得
  const [patternDetail, setPatternDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getPatternDetail = async () => {
      if (!patternId) {
        setError(new Error("パターンIDが指定されていません。"));
        setLoading(false);
        return;
      }
      try {
        // patternIdを指定して呼び出し、詳細データを取得
        const data = await fetchFourYearPatterns(patternId);
        setPatternDetail(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getPatternDetail();
  }, [patternId]);

  if (loading) {
    return <div className="loading">履修パターン詳細をロード中...</div>;
  }

  if (error) {
    return <div className="error">データのロードに失敗しました: {error.message}</div>;
  }

  if (!patternDetail) {
    return <div className="no-data">指定された履修パターンが見つかりませんでした。</div>;
  }

  const days = ['月', '火', '水', '木', '金'];
  const periods = ['1限', '2限', '3限', '4限', '5限'];

  return (
    <div className="four-year-pattern-detail">
      <h2>{patternDetail.name} の詳細</h2> {/* パターン名を表示 */}
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
                      {semester.schedule[day] && semester.schedule[day][period]
                        ? semester.schedule[day][period]
                        : ''}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
      <Link to="/patterns" className="back-link">パターン一覧に戻る</Link>
    </div>
  );
};

export default FourYearPatternDetail;