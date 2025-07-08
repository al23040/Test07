// src/components/W7_FourYearPatternDetail.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchFourYearPatterns } from '../api'; // 修正したAPI関数
import './W7_FourYearPatternDetail.css';

const W7_FourYearPatternDetail = () => {
  const { patternId } = useParams(); // URLから :patternId を取得
  const [pattern, setPattern] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 一覧画面と同様の仮ユーザー情報
  const userId = 12345;
  const userConditions = {
    min_units: 16,
    max_units: 20,
    preferences: ["balanced"],
  };

  useEffect(() => {
    // --- ここから追加 ---
    console.log("W7_FourYearPatternDetail: patternId from useParams:", patternId);
    // --- ここまで追加 ---

    const getPatternDetail = async () => {
      try {
        console.log(`詳細ページ: ${patternId} のデータを取得します。`); // 既存の行
        
        // --- ここから追加 ---
        console.log("W7_FourYearPatternDetail: Calling fetchFourYearPatterns with userId:", userId, "userConditions:", userConditions, "patternId:", patternId);
        // --- ここまで追加 ---

        // 修正したAPI関数に patternId を渡して詳細データを要求
        const data = await fetchFourYearPatterns(userId, userConditions, patternId);
        
        // --- ここから追加 ---
        console.log("W7_FourYearPatternDetail: APIから取得した詳細データ:", data);
        // --- ここまで追加 ---

        setPattern(data);
      } catch (err) {
        console.error("詳細データの取得でエラーが発生:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    getPatternDetail();
  }, [patternId]); // patternIdが変更されたら再実行

  if (loading) {
    return <div className="loading">パターン詳細をロード中...</div>;
  }

  if (error) {
    return <div className="error">詳細データのロードに失敗しました: {error.message}</div>;
  }

  if (!pattern) {
    return <div className="no-data">該当するパターンが見つかりませんでした。</div>;
  }

  // 時間割テーブルをレンダリングするヘルパーコンポーネント
  const Timetable = ({ schedule }) => (
    <table className="timetable">
      <thead>
        <tr>
          <th>時限</th>
          <th>月</th>
          <th>火</th>
          <th>水</th>
          <th>木</th>
          <th>金</th>
        </tr>
      </thead>
      <tbody>
        {['1限', '2限', '3限', '4限', '5限'].map(period => (
          <tr key={period}>
            <td>{period}</td>
            {['月', '火', '水', '木', '金'].map(day => (
              <td key={day}>{schedule[day]?.[period] || ''}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );

  return (
    <div className="four-year-pattern-detail">
      <h2>{pattern.name}</h2>
      <p className="description">{pattern.description}</p>
      <p className="total-units">総取得単位数: {pattern.totalUnits}単位</p>

      {pattern.semesters.map((semester, index) => (
        <div key={index} className="semester-schedule">
          <h4>{semester.year}年度 {semester.semester}</h4>
          <Timetable schedule={semester.schedule} />
        </div>
      ))}
      
      <Link to="/patterns" className="back-link">
        パターン一覧に戻る
      </Link>
    </div>
  );
};

export default W7_FourYearPatternDetail;