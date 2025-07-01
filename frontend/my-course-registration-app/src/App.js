// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import GradeUploadPage from './components/W3_GradeUploadPage';
import SubjectConfirmationPage from './components/W4_SubjectConfirmationPage';
import SubjectEditPage from './components/W5_SubjectEditPage';
import PatternDisplay from './components/FourYearPatternList'; // W7コンポーネントをインポート
import CurrentSemesterRecommendation from './components/CurrentSemesterRecommendation'; // W8コンポーネントをインポート
import './App.css'; // グローバルなスタイル

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="main-nav">
          <ul>
            <li>
              <Link to="/grade-upload">W3 成績通知書アップロード</Link>
            </li>
            <li>
              <Link to="/subject-confirmation">W4 履修科目確認</Link>
            </li>
            <li>
              <Link to="/subject-edit">W5 履修科目編集</Link>
            </li>
            <li>
              <Link to="/patterns">W7 履修パターン表示</Link> {/* W7へのリンクを追加 */}
            </li>
            <li>
              <Link to="/current-semester-recommendation">W8 今学期のおすすめ</Link> {/* W8へのリンクを追加 */}
            </li>
          </ul>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/grade-upload" element={<GradeUploadPage />} />
            <Route path="/subject-confirmation" element={<SubjectConfirmationPage />} />
            <Route path="/subject-edit" element={<SubjectEditPage />} />
            <Route path="/patterns" element={<PatternDisplay />} /> {/* W7のルートを追加 */}
            <Route path="/current-semester-recommendation" element={<CurrentSemesterRecommendation />} /> {/* W8のルートを追加 */}
            {/* デフォルトルート（任意のページにリダイレクトまたはホーム画面表示） */}
            <Route path="/" element={<Home />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div className="home-container">
      <h2>履修登録補助システム</h2>
      <p>左のナビゲーションから各画面へアクセスしてください。</p>
    </div>
  );
}

export default App;