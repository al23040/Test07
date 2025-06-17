// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PatternDisplay from './components/PatternDisplay'; // W7
import CurrentSemesterRecommendation from './components/CurrentSemesterRecommendation'; // W8
// 他のコンポーネントは省略

import './App.css';

function App() {
  return (
    <Router>
      <header className="app-header">
        <h1>履修登録補助システム</h1>
        <nav className="main-nav">
          <ul>
            {/* 開発中のナビゲーションリンク */}
            <li><Link to="/recommendation-semester">今学期のおすすめ (W8)</Link></li> {/* W8への直接リンク */}
            <li><Link to="/patterns">履修パターン候補 (W7)</Link></li>
            {/* 実際のアプリケーションでは、W6からW8へ遷移し、W8からW7へ遷移する */}
          </ul>
        </nav>
      </header>

      <main className="app-main">
        <Routes>
          {/* ルートパスにアクセスした場合、仮にW8を表示する（W6は未実装のため） */}
          <Route path="/" element={<CurrentSemesterRecommendation />} />
          <Route path="/recommendation-semester" element={<CurrentSemesterRecommendation />} /> {/* W8 */}
          <Route path="/patterns" element={<PatternDisplay />} /> {/* W7 */}
          {/* 他のルート */}
        </Routes>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 履修登録補助システム 7班</p>
      </footer>
    </Router>
  );
}

export default App;