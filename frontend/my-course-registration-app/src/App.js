// src/App.js
/*import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import Login from './components/W1_Login';
import SignUp from './components/W2_SignUp';
import GradeUploadPage from './components/W3_GradeUploadPage';
import SubjectConfirmationPage from './components/W4_SubjectConfirmationPage';
import SubjectEditPage from './components/W5_SubjectEditPage';
import PatternDisplay from './components/W7_FourYearPatternList';
import CurrentSemesterRecommendation from './components/W8_CurrentSemesterRecommendation';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="main-nav">
          <ul>
            <li><Link to="/login">ログイン</Link></li>
            <li><Link to="/register">登録</Link></li>
            <li><Link to="/grade-upload">成績アップロード</Link></li>
            <li><Link to="/subject-confirmation">履修科目確認</Link></li>
            <li><Link to="/subject-edit">履修科目編集</Link></li>
            <li><Link to="/patterns">履修パターン表示</Link></li>
            <li><Link to="/current-semester-recommendation">今学期のおすすめ</Link></li>
          </ul>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<SignUp />} />
            <Route path="/grade-upload" element={<GradeUploadPage />} />
            <Route path="/subject-confirmation" element={<SubjectConfirmationPage />} />
            <Route path="/subject-edit" element={<SubjectEditPage />} />
            <Route path="/patterns" element={<PatternDisplay />} />
            <Route path="/current-semester-recommendation" element={<CurrentSemesterRecommendation />} />
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

export default App;*/

// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoute from './components/PrivateRoute';

import Login from './components/W1_Login';
import SignUp from './components/W2_SignUp';
import GradeUploadPage from './components/W3_GradeUploadPage';
import SubjectConfirmationPage from './components/W4_SubjectConfirmationPage';
import SubjectEditPage from './components/W5_SubjectEditPage';
import PreferenceInput from './components/W6_PreferenceInput';
import PatternDisplay from './components/W7_FourYearPatternList';
import CurrentSemesterRecommendation from './components/W8_CurrentSemesterRecommendation';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <nav className="main-nav">
            <ul>
              <li><Link to="/login">ログイン</Link></li>
              <li><Link to="/register">登録</Link></li>
              <li><Link to="/grade-upload">成績アップロード</Link></li>
              <li><Link to="/subject-confirmation">履修科目確認</Link></li>
              <li><Link to="/subject-edit">履修科目編集</Link></li>
              <li><Link to="/preference-input">希望条件</Link></li>
              <li><Link to="/patterns">履修パターン表示</Link></li>
              <li><Link to="/current-semester-recommendation">今学期のおすすめ</Link></li>
            </ul>
          </nav>

          <div className="content">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<SignUp />} />

              {/* 保護されたルート（ログイン必須） */}
              <Route path="/grade-upload" element={
                <PrivateRoute><GradeUploadPage /></PrivateRoute>
              } />
              <Route path="/subject-confirmation" element={
                <PrivateRoute><SubjectConfirmationPage /></PrivateRoute>
              } />
              <Route path="/subject-edit" element={
                <PrivateRoute><SubjectEditPage /></PrivateRoute>
              } />
              <Route path="/preference-input" element={
                <PrivateRoute><PreferenceInput /></PrivateRoute>
              } />
              <Route path="/patterns" element={
                <PrivateRoute><PatternDisplay /></PrivateRoute>
              } />
              <Route path="/current-semester-recommendation" element={
                <PrivateRoute><CurrentSemesterRecommendation /></PrivateRoute>
              } />

              <Route path="/" element={<Home />} />
            </Routes>
          </div>
        </div>
      </Router>
    </AuthProvider>
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
