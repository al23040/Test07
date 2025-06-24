// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import CurrentSemesterRecommendation from './components/CurrentSemesterRecommendation';
import FourYearPatternList from './components/FourYearPatternList';
import FourYearPatternDetail from './components/FourYearPatternDetail';
import './App.css'; // 必要に応じてCSSファイルを作成

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>履修登録補助システム</h1>
          <nav>
            <ul>
              <li><Link to="/">今学期のおすすめ</Link></li>
              <li><Link to="/patterns">履修登録パターン</Link></li>
            </ul>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<CurrentSemesterRecommendation />} />
            <Route path="/patterns" element={<FourYearPatternList />} />
            <Route path="/patterns/:patternId" element={<FourYearPatternDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;