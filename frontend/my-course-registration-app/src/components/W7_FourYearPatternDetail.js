/*// frontend/my-course-registration-app/src/components/W7_FourYearPatternDetail.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchFourYearPatternDetail } from '../api'; // 作成したAPI関数をインポート
import './W7_FourYearPatternDetail.css'; // 対応するCSSファイルをインポート

const W7_FourYearPatternDetail = () => {
  const { patternId } = useParams(); // URLからパターンIDを取得 (例: /patterns/dummy_pattern_1)
  const [patternDetail, setPatternDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getDetail = async () => {
      setLoading(true);
      try {
        const data = await fetchFourYearPatternDetail(patternId);
        setPatternDetail(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getDetail();
  }, [patternId]); // patternIdが変わったら再取得

  if (loading) {
    return <div className="loading-container"><div className="loader"></div><p>パターン詳細を読み込み中...</p></div>;
  }
  if (error) {
    return <div className="error-container"><p>エラー: {error.message}</p></div>;
  }
  if (!patternDetail) {
    return <p>パターンの詳細が見つかりません。</p>;
  }

  return (
    <div className="pattern-detail-container">
      <header className="pattern-detail-header">
        <h1>{patternDetail.name}</h1>
        <p className="pattern-description">{patternDetail.description}</p>
        <div className="pattern-meta">
          <span>総単位数: <strong>{patternDetail.totalUnits}</strong></span>
        </div>
      </header>

      <div className="semesters-grid">
        {patternDetail.semesters.map((semester, index) => (
          <section key={index} className="semester-card">
            <h3>{semester.year}年次 {semester.semester}</h3>
            <ul className="course-list-detail">
              {semester.courses.map((course, courseIndex) => (
                <li key={courseIndex}>
                  <span className="course-name">{course.name}</span>
                  <span className="course-credits">{course.credits}単位</span>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>

      <footer className="pattern-detail-footer">
        <Link to="/patterns" className="back-link">← パターン一覧へ戻る</Link>
      </footer>
    </div>
  );
};

export default W7_FourYearPatternDetail;*/

import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import './W7_FourYearPatternDetail.css';

const W7_FourYearPatternDetail = () => {
  const { patternId } = useParams();
  const [patternDetail, setPatternDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDetail = () => {
      const storedPatterns = localStorage.getItem('four_year_patterns');
      if (!storedPatterns) {
        setPatternDetail(null);
        setLoading(false);
        return;
      }
      const patterns = JSON.parse(storedPatterns);
      const found = patterns.find((pattern) => String(pattern.id) === String(patternId));
      setPatternDetail(found || null);
      setLoading(false);
    };

    loadDetail();
  }, [patternId]);

  if (loading) {
    return React.createElement(
      'div',
      { className: 'loading-container' },
      React.createElement('div', { className: 'loader' }),
      React.createElement('p', null, 'パターン詳細を読み込み中...')
    );
  }

  if (!patternDetail) {
    return React.createElement('p', null, 'パターンの詳細が見つかりません。');
  }

  return React.createElement(
    'div',
    { className: 'four-year-pattern-detail' },
    React.createElement(
      'header',
      { className: 'pattern-detail-header' },
      React.createElement('h1', null, patternDetail.name),
      React.createElement('p', { className: 'description' }, patternDetail.description),
      React.createElement(
        'div',
        { className: 'total-units' },
        React.createElement('span', null, '総単位数: ', React.createElement('strong', null, patternDetail.totalUnits))
      )
    ),
    React.createElement(
      'div',
      { className: 'semesters-grid' },
      (patternDetail.semesters || []).map((semester, index) => 
        React.createElement(
          'section',
          { key: index, className: 'semester-schedule' },
          React.createElement('h4', null, semester.year + '年次 ' + semester.semester),
          React.createElement(
            'table',
            { className: 'timetable' },
            React.createElement(
              'thead',
              null,
              React.createElement(
                'tr',
                null,
                React.createElement('th', null, '科目名'),
                React.createElement('th', null, '単位数')
              )
            ),
            React.createElement(
              'tbody',
              null,
              semester.courses.map((course, i) =>
                React.createElement(
                  'tr',
                  { key: i },
                  React.createElement('td', null, course.subject_name),
                  React.createElement('td', null, course.credit)
                )
              )
            )
          )
        )
      )
    ),
    React.createElement(
      'footer',
      { className: 'pattern-detail-footer' },
      React.createElement(Link, { to: '/patterns', className: 'back-link' }, '← パターン一覧へ戻る')
    )
  );
};

export default W7_FourYearPatternDetail;
