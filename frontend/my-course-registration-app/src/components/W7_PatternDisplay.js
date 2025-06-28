// src/components/PatternDisplay.js
import React, { useState } from 'react'; // useEffectは不要になるため削除
import PatternCard from './W7_PatternCard';
import './W7_PatternDisplay.css'; // 新しくCSSファイルを作成します

function PatternDisplay() {
  // ダミーデータ
  const dummyPatterns = [
    {
      id: 1,
      totalUnits: 124,
      remainingUnits: 12,
      itSkillAcquisitionRate: 85,
      description: '情報科学系の基礎から応用までバランス良く学べます。',
      coreCourses: ['データ構造とアルゴリズム', 'オペレーティングシステム'],
      electiveCourses: ['機械学習入門', 'Webアプリケーション開発'],
      remarks: '情報技術者試験の対策も考慮されたパターンです。'
    },
    {
      id: 2,
      totalUnits: 128,
      remainingUnits: 8,
      itSkillAcquisitionRate: 92,
      description: 'AI・データサイエンス分野に特化した専門的な履修計画です。',
      coreCourses: ['応用統計学', '深層学習'],
      electiveCourses: ['ビッグデータ解析', '自然言語処理'],
      remarks: '大学院進学を目指す方にもおすすめです。'
    },
    {
      id: 3,
      totalUnits: 126,
      remainingUnits: 10,
      itSkillAcquisitionRate: 78,
      description: 'ネットワーク・セキュリティ分野に重点を置いた履修計画です。',
      coreCourses: ['コンピュータネットワーク', '情報セキュリティ'],
      electiveCourses: ['暗号理論', 'デジタルフォレンジック'],
      remarks: 'セキュリティエンジニアを目指す方におすすめです。'
    },
  ];

  // patterns stateをダミーデータで初期化
  const [patterns, setPatterns] = useState(dummyPatterns);
  // エラー状態を管理するstateも追加（代替フローのために必要）
  const [showNoPatternsMessage, setShowNoPatternsMessage] = useState(false);

  // 表示するパターンがない場合のメッセージをテストするために、
  // このボタンを押すとパターンが非表示になるようにします。
  const toggleNoPatternsMessage = () => {
    setShowNoPatternsMessage(!showNoPatternsMessage);
    if (!showNoPatternsMessage) {
      setPatterns([]); // パターンを空にしてメッセージを表示
    } else {
      setPatterns(dummyPatterns); // 元に戻す
    }
  };

  const handleViewDetails = (patternId) => {
    // 実際には詳細画面（W8など）に遷移するロジックをここに書きます
    // 例: navigate(`/pattern-detail/${patternId}`); (react-router-dom v6)
    console.log(`パターン ${patternId} の詳細を表示（W8に相当する画面へ遷移）`);
    alert(`パターン ${patternId} の詳細を表示します。\n（W8などの詳細画面へ遷移する想定）`);
  };

  const handleGoBackToConditions = () => {
    console.log('希望条件のページに戻る（W6に相当する画面へ遷移）');
    alert('希望条件の入力ページに戻ります。\n（W6などへ遷移する想定）');
  };

  return (
    <div className="pattern-display-container">
      <h2>履修登録パターンの候補</h2>

      {/* テスト用のボタン: 表示するパターンがない場合の挙動を確認できます */}
      <button onClick={toggleNoPatternsMessage} className="test-button">
        {showNoPatternsMessage ? 'パターンを表示' : 'パターンを非表示（代替フローテスト）'}
      </button>

      {patterns.length > 0 && !showNoPatternsMessage ? (
        <div className="pattern-list">
          {patterns.map(pattern => (
            <PatternCard
              key={pattern.id}
              pattern={pattern}
              onViewDetails={handleViewDetails}
            />
          ))}
        </div>
      ) : (
        // 代替フロー: 表示するパターンがない場合
        <div className="no-patterns-message">
          <p>表示するパターンがありません。希望条件の変更をお願いします。</p>
          <button onClick={handleGoBackToConditions} className="back-button">
            希望条件のページに戻る
          </button>
        </div>
      )}
    </div>
  );
}

export default PatternDisplay;